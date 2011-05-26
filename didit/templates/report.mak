Category '${category}' over timespan '${str(timespan)}'
${'-'*len("Category '" + category + "' last " + str(timespan) + " days")}
<% printed = {} %>
% for key in sorted(data.keys()):
<% fmt_key = key.strftime("%Y-%m-%d") %>
% if not fmt_key in printed:
<% printed[fmt_key] = True %>
----

${fmt_key}:

% endif
  - ${data[key]}
% endfor
