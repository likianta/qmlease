from lk_utils import fs
from lk_utils import textwrap as tw

keys = (
    'primary',
    'on_primary',
    'primary_container',
    'on_primary_container',
    'secondary',
    'on_secondary',
    'secondary_container',
    'on_secondary_container',
    'tertiary',
    'on_tertiary',
    'tertiary_container',
    'on_tertiary_container',
    'error',
    'on_error',
    'error_container',
    'on_error_container',
    'background',
    'on_background',
    'surface',
    'on_surface',
    'surface_variant',
    'on_surface_variant',
    'outline',
    'outline_variant',
    'shadow',
    'scrim',
    'inverse_surface',
    'inverse_on_surface',
    'inverse_primary',
    'surface_dim',
    'surface_bright',
    'surface_container_lowest',
    'surface_container_low',
    'surface_container',
    'surface_container_high',
    'surface_container_highest',
)

template = tw.wrap(
    '''
    class Color(QObject):
        ...

        # copy the following lines, and paste them to `qmlease/style/color2.py`.
        {}
    '''
)

property_lines = []
for key in keys:
    property_lines.append(
        tw.wrap(
            '''
            {} = Property(
                str,
                partial(_qget_color, name='{}'),
                notify=current_scheme_changed
            )
            '''
        ).format(key, key)
    )

output = template.format(tw.join(property_lines, 4))
fs.dump(output, fs.xpath('_codegen_result.txt'))
