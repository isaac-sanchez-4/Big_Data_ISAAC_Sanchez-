SELECT SERVERPROPERTY('ProductMajorVersion') AS version_principal,
       compatibility_level
FROM sys.databases
WHERE name = N'SonoraDB';