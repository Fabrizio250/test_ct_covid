# Software List

> List all your software which you use either in your Quality Management System or as part of your product
> development. Typically, those include Slack, GitHub, your IDE (e.g., IntelliJ) and programming libraries
> which you (only) use during development.
>
> Libraries which you include in your product (i.e., which are deployed with it) don't belong here. They belong
> in the SOUP list.



| ID | Name          | Manufacturer     | Bug tracker URL                            | Needs validation? | Next validation | Last validation | Decommissioning |
|----|---------------|------------------|--------------------------------------------|-------------------|-----------------|-----------------|-----------------|
{% for software in software_list %} | {{ software.ID }}  | {{ software.Name }} | {{ software.Manufacturer }} | {{ software.get('Bug tracker URL', '') }} | {{ software.get('Needs validation?', '') }} | {{ software.get('Next validation', '') }} | {{ software.get('Last validation', '') }} | {{ software.get('Decommissioning', '') }} |
{% endfor %}

---


Template Copyright [openregulatory.com](https://openregulatory.com). See [template
license](https://openregulatory.com/template-license).

Please don't remove this notice even if you've modified contents of this template.