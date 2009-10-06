// lino/includes/container.js
new {{element.ext_container}}({
  layout: '{{element.ext_layout}}',
  items: [
  {% for e in element.children %}
      {{e.as_ext}},
  {% endfor %}
  ]
});