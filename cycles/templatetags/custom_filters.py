from django import template

register = template.Library()

@register.filter
def div(value, arg):
    try:
        return float(value) / float(arg)
    except (ValueError, TypeError):
        return None
    except ZeroDivisionError:
        return 0

@register.filter
def mul(value, arg):
    try:
        result = float(value) * float(arg)
        return int(result) if result == int(result) else result
    except (ValueError, TypeError):
        return None

@register.filter
def sub(value, arg):
    try:
        result = float(value) - float(arg)
        return int(result) if result == int(result) else result
    except (ValueError, TypeError):
        return None

@register.filter
def floatformat(value, arg=0):
    try:
        return f'{float(value):.{int(arg)}f}'
    except (ValueError, TypeError):
        return None

@register.filter
def mod(value, arg):
    try:
        return int(value) % int(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def color_hex(color_name, shade):
    palette = {
        'blue': {'50': '#eff6ff', '100': '#dbeafe', '800': '#1e40af'},
        'green': {'50': '#f0fdf4', '100': '#dcfce7', '800': '#166534'},
        'yellow': {'50': '#fefce8', '100': '#fef9c3', '800': '#854d0e'},
        'orange': {'50': '#fff7ed', '100': '#ffedd5', '800': '#9a3412'},
        'purple': {'50': '#faf5ff', '100': '#f3e8ff', '800': '#6b21a8'},
        'indigo': {'50': '#eef2ff', '100': '#e0e7ff', '800': '#3730a3'},
        'red': {'50': '#fef2f2', '100': '#fee2e2', '800': '#991b1b'},
        'gray': {'50': '#f9fafb', '100': '#f3f4f6', '800': '#1f2937'},
    }
    return palette.get(color_name, {}).get(shade, '#f9fafb')
