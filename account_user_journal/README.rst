Restrict Journal for Users
==========================
El usuario solo usa sus diarios permitidos.

Versión modificada (lógica invertida): en vez de elegir los diarios prohibidos,
se eligen los diarios que el usuario sí puede usar.

Configuración
=============
Ajustes → Usuarios → (usuario) → pestaña **Diarios permitidos**.

- De cada tipo de diario elegido (Ventas, Efectivo, Banco...), el usuario solo puede
  usar los elegidos. Los tipos sin ninguno elegido quedan libres.
- Vacío: el usuario puede usar todos los diarios (como sin el módulo).

Qué hace
========
- Factura: la lista de diarios solo muestra los permitidos y la factura nueva ya sale
  con el diario permitido del usuario.
- Factura o pago en un diario no permitido: error.
- Registrar pago: solo salen los diarios permitidos.

Sucker Punch (punto de venta) lee los diarios permitidos del usuario que entra y
factura y cobra con ellos.

License
=======
GNU Lesser General Public License, Version 3 (LGPL v3).
(https://www.gnu.org/licenses/lgpl-3.0-standalone.html)

Credits
=======
Developers: Cybrosys Techno Solutions <https://www.cybrosys.com>
