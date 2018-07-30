{{ fullname | escape | underline}}

.. currentmodule:: {{ module }}

.. autoclass:: {{ objname }}

  {% block methods %}
  {% if methods %}
  .. rubric:: Methods

  .. autosummary::
    :nosignatures:
  {% for item in methods %}
     ~{{ name }}.{{ item }}
  {%- endfor %}
  {% endif %}

  {% for item in methods %}
  .. automethod:: {{item}}
  {%- endfor%}
  {% endblock %}

  {% block attributes %}
  {% if attributes %}
  .. rubric:: Attributes

  .. autosummary::
  {% for item in attributes %}
    ~{{ name }}.{{ item }}
  {%- endfor %}
  {% endif %}
  {% endblock %}