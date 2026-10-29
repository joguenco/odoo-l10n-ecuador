## Module <account_restrict_journal>

#### 28.10.2026
#### Version 19.0.2.0.0
#### IMP

- Lógica invertida: en el usuario se eligen los «Diarios permitidos» (por tipo de
  diario) en vez de los prohibidos.
- La factura nueva ya sale con el diario permitido del usuario.
- Validaciones con constrains en vez de sobrescribir create/write de los pagos (el
  create original fallaba si el pago no traía diario).
- «Registrar pago» usa la lógica de Odoo 19 y después filtra (antes dejaba fuera los
  diarios de tipo «credit»).
- Se quitan el grupo «Restrict Journals», sus reglas de registro y el campo calculado
  que lanzaba error al abrir una factura.

#### 04.08.2026
#### Version 19.0.1.0.0
#### ADD

- Initial release of Restrict Journal for Users.
- User can select only allowed journals
