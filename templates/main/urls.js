var URLS = {
	{% for item in urls %}
		{{ item.0 }}: "{{ item.1 }}"{% if not forloop.last %},{% endif %}
	{% endfor %}
}