from django import template


register = template.Library()


BLACK_WORDS = ['article1', 'header2']


@register.filter()
def censor(value):
   newvalue = value
   for bw in BLACK_WORDS:
      nw = bw[0] + ("*" * (len(bw)-1))
      newvalue = newvalue.replace(bw, nw)
      newvalue = newvalue.replace(bw.title(), nw.title())
   return newvalue