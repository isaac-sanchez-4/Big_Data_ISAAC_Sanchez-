BEGIN TRAN;
    UPDATE dbo.usuarios 
    SET plan_suscripcion = N'Premium' 
    WHERE usuario_id = 2;
    
    SELECT plan_suscripcion AS [Plan Dentro Transaccion]
    FROM dbo.usuarios WHERE usuario_id = 2;
ROLLBACK TRAN;

SELECT plan_suscripcion AS [Plan Tras Rollback]
FROM dbo.usuarios WHERE usuario_id = 2;