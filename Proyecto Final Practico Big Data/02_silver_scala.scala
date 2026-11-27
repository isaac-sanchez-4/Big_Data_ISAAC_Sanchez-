@'
import org.apache.spark.sql.functions._
import java.sql.{Date, Timestamp}
import java.time.LocalDate
import spark.implicits._

spark.sparkContext.setLogLevel("ERROR")
spark.sql("USE iberian_logistics_db")

case class CustomerRaw(
  customer_id: String,
  full_name: String,
  email: String,
  city: String,
  segment: String,
  age: Option[Long],
  signup_date: String,
  _ingestion_timestamp: java.sql.Timestamp,
  _source_file: String
)

case class CustomerSilver(
  customer_id: String,
  full_name: String,
  email: String,
  city: String,
  segment: String,
  age: Int,
  signup_date: java.sql.Date,
  processed_at: java.sql.Timestamp
)

case class OrderRaw(
  order_id: String,
  customer_id: String,
  order_date: String,
  product_category: String,
  quantity: Option[Long],
  unit_price: Option[Double],
  shipping_cost: Option[Double],
  carrier: String,
  delivery_status: String,
  promised_delivery_days: Option[Long],
  actual_delivery_days: Option[Long],
  _ingestion_timestamp: java.sql.Timestamp,
  _source_file: String
)

case class OrderSilver(
  order_id: String,
  customer_id: String,
  order_date: java.sql.Date,
  product_category: String,
  quantity: Int,
  unit_price: Double,
  shipping_cost: Double,
  gross_amount: Double,
  total_order_value: Double,
  carrier: String,
  delivery_status: String,
  promised_delivery_days: Int,
  actual_delivery_days: Int,
  delay_days: Int,
  is_on_time: Boolean,
  processed_at: java.sql.Timestamp
)

object SilverRules extends Serializable {
  def isValidCustomer(c: CustomerRaw): Boolean = {
    val validId = c.customer_id != null && c.customer_id.trim.nonEmpty
    val validAge = c.age.exists(a => a >= 18 && a <= 100)
    validId && validAge
  }

  def toCustomerSilver(c: CustomerRaw): CustomerSilver = {
    val rawSeg = if (c.segment == null) "" else c.segment.trim.toUpperCase.replace("Á", "A").replace("É", "E").replace("Í", "I").replace("Ó", "O").replace("Ú", "U")
    val normSegment = rawSeg match {
      case "VIP"    => "VIP"
      case "BASICO" => "BASICO"
      case _        => "ESTANDAR"
    }
    val normEmail = if (c.email != null && c.email.contains("@")) c.email.trim.toLowerCase else "sin_email@invalido.es"
    CustomerSilver(
      customer_id = c.customer_id.trim,
      full_name = if (c.full_name != null) c.full_name.trim else "Desconocido",
      email = normEmail,
      city = if (c.city != null) c.city.trim else "Desconocida",
      segment = normSegment,
      age = c.age.get.toInt,
      signup_date = Date.valueOf(LocalDate.parse(c.signup_date)),
      processed_at = new Timestamp(System.currentTimeMillis())
    )
  }

  def isValidOrder(o: OrderRaw): Boolean = {
    val validOrderId = o.order_id != null && o.order_id.trim.nonEmpty
    val validCustId = o.customer_id != null && o.customer_id.trim.nonEmpty
    val validQty = o.quantity.exists(_ > 0)
    val validPrice = o.unit_price.exists(_ > 0.0)
    validOrderId && validCustId && validQty && validPrice
  }

  def toOrderSilver(o: OrderRaw): OrderSilver = {
    val qty = o.quantity.get.toInt
    val price = o.unit_price.get
    val ship = o.shipping_cost.getOrElse(0.0)
    val gross = Math.round(qty * price * 100.0) / 100.0
    val total = Math.round((gross + ship) * 100.0) / 100.0
    val promised = o.promised_delivery_days.getOrElse(3L).toInt
    val actual = o.actual_delivery_days.map(_.toInt).getOrElse(promised)
    val delay = actual - promised
    val onTime = actual <= promised
    val normStatus = if (o.delivery_status != null) o.delivery_status.trim.toUpperCase else "UNKNOWN"
    OrderSilver(
      order_id = o.order_id.trim,
      customer_id = o.customer_id.trim,
      order_date = Date.valueOf(LocalDate.parse(o.order_date)),
      product_category = if (o.product_category != null) o.product_category.trim else "Otros",
      quantity = qty,
      unit_price = price,
      shipping_cost = ship,
      gross_amount = gross,
      total_order_value = total,
      carrier = if (o.carrier != null) o.carrier.trim else "Desconocido",
      delivery_status = normStatus,
      promised_delivery_days = promised,
      actual_delivery_days = actual,
      delay_days = delay,
      is_on_time = onTime,
      processed_at = new Timestamp(System.currentTimeMillis())
    )
  }
}

val silverPathBase = "/opt/datos/iberian_logistics_polyglot/silver"

val dsCustomersRaw = spark.table("iberian_logistics_db.bronze_customers").as[CustomerRaw]
val dsCustomersSilver = dsCustomersRaw.filter(SilverRules.isValidCustomer _).dropDuplicates("customer_id").map(SilverRules.toCustomerSilver _)
dsCustomersSilver.write.format("parquet").mode("overwrite").option("path", s"$silverPathBase/customers").saveAsTable("iberian_logistics_db.silver_customers")

val dsOrdersRaw = spark.table("iberian_logistics_db.bronze_orders_shipments").as[OrderRaw]
val dsOrdersClean = dsOrdersRaw.filter(SilverRules.isValidOrder _).dropDuplicates("order_id").map(SilverRules.toOrderSilver _)
val dsCustomersSilverSaved = spark.table("iberian_logistics_db.silver_customers").as[CustomerSilver]
val dsOrdersSilverValid = dsOrdersClean.joinWith(dsCustomersSilverSaved, dsOrdersClean("customer_id") === dsCustomersSilverSaved("customer_id"), "inner").map(_._1)
dsOrdersSilverValid.write.format("parquet").mode("overwrite").option("path", s"$silverPathBase/orders_shipments").saveAsTable("iberian_logistics_db.silver_orders_shipments")

println("=================================================================")
println(s"Total Clientes en Silver        : ${spark.table("iberian_logistics_db.silver_customers").count()}")
println(s"Total Pedidos Válidos en Silver : ${spark.table("iberian_logistics_db.silver_orders_shipments").count()}")
println("=================================================================")

spark.stop()
sys.exit(0)
'@ | Set-Content -Encoding UTF8 .\notebooks\02_silver_scala.scala