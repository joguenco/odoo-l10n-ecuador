# Migraciones
Recursos para migrar módulos de Odoo a una nueva versión.

## odoo-module-migrator 
Es una librería en python para migrar automáticamente un módulo, haciendo compatible el código fuente con la nuevas versiones de Odoo.

- En el directorio raíz clonar la librería
```
git clone https://github.com/OCA/odoo-module-migrator.git
```
- Instalar
```
pip install ./odoo-module-migrator
```
- Ejemplo de uso
```
odoo-module-migrate
    --directory             ./
    --modules               pos_order_pricelist_change
    --init-version-name     8.0
    --target-version-name   12.0
    --format-patch
```
- Ejecución
```

```