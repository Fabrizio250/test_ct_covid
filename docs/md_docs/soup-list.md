# SOUP List (Software of Unknown Provenance)

> The 62304 requires you to document your SOUP, which is short for Software of Unknown Provenance. In human
> language, those are the third-party libraries you're using in your code, typically in your
> `requirements.txt` or `Gemfile`.

| Classes | IEC 62304:2006 Section                          | Document Section |
|---------|-------------------------------------------------|------------------|
| B, C    | 5.3.3 (Functional and Performance Requirements) | 2                |
| B, C    | 5.3.4 (Hardware and Software Requirements)      | 2                |
| B, C    | 7.1.2 (Hazardous Situations)                    | 2                |
| B, C    | 7.1.3 (SOUP Anomaly Lists)                      | 2                |
| A, B, C | 8.1.2 (Identify SOUP)                           | 2                |

## 1 Risk Level Definitions

> The 62304 requires you to assess risks associated with SOUP. The simplest way to do this is to classify each
> SOUP as a certain risk level. Unless you're developing software which shoots radiation at patients, it's
> likely that your SOUP risk levels remain "low" or "medium".

| Risk Level | Definition                                                 |
|------------|------------------------------------------------------------|
| Low        | Malfunction in SOUP can't lead to patient harm.            |
| Medium     | Malfunction in SOUP can lead to reversible patient harm.   |
| High       | Malfunction in SOUP can lead to irreversible patient harm. |

## 2 SOUP List

> This is the actual SOUP list. For each third-party library you use, add an entry in the table below. The
> idea is to only have one "global" SOUP list for your medical device even though the code may actually live
> in multiple repositories. That's what the "software system" column is for; you could also mention your (git)
> repository there.

> When specifying requirements, the 62304 requires you to mention functional, performance, hard- and software
> requirements. However, you may not have to re-state certain requirements if they apply to all SOUP,
> e.g., "runs on Linux". So prefer to keep the requirements simple, in a way in which you would communicate them
> to colleagues on your development team when answering the question "why did we import this library?".

> As with all templates: It's more about the content (i.e., the columns you see below) than the tool (filling
> this out in Google sheets / markdown / wherever). Nobody says that you have to maintain this as a Google
> sheet. If you can find a way to integrate this in your workflow in a better way, e.g., in a markdown file in
> your git repository, go for it! Just keep in mind that you need to be able to export it to send it to
> auditors.

| ID | Software System | Package Name | Programming Language | Version | Website                                          | Last verified at | Risk Level | Requirements               | Verification Reasoning                                                    |
|----|-----------------|--------------|----------------------|---------|--------------------------------------------------|------------------|------------|----------------------------|---------------------------------------------------------------------------|
| 1 | Unknown |  | Unknown | unknown | [unknown](unknown) | Unknown | unknown | unknown | unknown |
| 2 | Unknown | cv2 | Unknown | unknown | [unknown](unknown) | Unknown | unknown | unknown | unknown |
| 3 | OS Independent | fastapi | Python | 0.115.0 | [unknown](unknown) | 2024-09-17 | N/A | N/A | N/A |
| 4 | MacOS | scipy | Python | 1.13.1 | [https://scipy.org/](https://scipy.org/) | 2024-08-21 | N/A | N/A | N/A |
| 5 | Unknown | time | Unknown | unknown | [unknown](unknown) | Unknown | unknown | unknown | unknown |
| 6 | OS Independent | uvicorn | Python | 0.31.0 | [unknown](unknown) | 2024-09-27 | N/A | N/A | N/A |
| 7 | Unknown | covidx | Unknown | unknown | [unknown](unknown) | Unknown | unknown | unknown | unknown |
| 8 | Unknown | PIL | Python | unknown | [unknown](unknown) | Unknown | unknown | unknown | unknown |
| 9 | OS Independent | locust | Python | unknown | [unknown](unknown) | 2024-09-28 | unknown | unknown | unknown |
| 10 | Unknown | itertools | Unknown | unknown | [unknown](unknown) | Unknown | unknown | unknown | unknown |
| 11 | MacOS | numpy | Python | 2.0.2 | [https://numpy.org](https://numpy.org) | 2024-09-03 | N/A | N/A | N/A |
| 12 | Unknown | torch | Unknown | 2.4.1 | [https://pytorch.org/](https://pytorch.org/) | 2024-09-04 | N/A | N/A | N/A |
| 13 | Unknown | matplotlib | Python | 3.9.2 | [unknown](unknown) | 2024-08-13 | N/A | N/A | N/A |
| 14 | OS Independent | monitoring | Python | unknown | [unknown](unknown) | 2019-07-02 | unknown | unknown | unknown |
| 15 | Unknown | sklearn | Python | unknown | [unknown](unknown) | 2023-12-01 | unknown | unknown | unknown |
| 16 | MacOS | pytest | Only | unknown | [unknown](unknown) | 2024-09-10 | unknown | unknown | unknown |
| 17 | Unknown | yaml | Python | unknown | [unknown](unknown) | Unknown | unknown | unknown | unknown |
| 18 | Unknown | prometheus-fastapi-instrumentator | Python | 7.0.0 | [https://github.com/trallnag/prometheus-fastapi-instrumentator](https://github.com/trallnag/prometheus-fastapi-instrumentator) | 2024-03-13 | N/A | N/A | N/A |
| 19 | MacOS | tqdm | Python | 4.66.5 | [unknown](unknown) | 2024-08-03 | N/A | N/A | N/A |
| 20 | Unknown | api | Unknown | unknown | [unknown](unknown) | 2017-11-08 | unknown | unknown | unknown |
| 21 | OS Independent | evaluate | 3 | unknown | [unknown](unknown) | 2024-09-11 | unknown | unknown | unknown |
| 22 | OS Independent | seaborn | Python | 0.13.2 | [unknown](unknown) | 2024-01-25 | N/A | N/A | N/A |
| 23 | OS Independent | pandas | Python | 2.2.3 | [https://pandas.pydata.org](https://pandas.pydata.org) | 2024-09-20 | N/A | N/A | N/A |
| 24 | Unknown | prometheus_client | Python | 0.21.0 | [https://github.com/prometheus/client_python](https://github.com/prometheus/client_python) | 2024-09-20 | N/A | N/A | N/A |
| 25 | Unknown | torchvision | Python | 0.19.1 | [https://github.com/pytorch/vision](https://github.com/pytorch/vision) | 2024-09-04 | N/A | N/A | N/A |
| 26 | Unknown | utils_test | Unknown | unknown | [unknown](unknown) | Unknown | unknown | unknown | unknown |
| 27 | Unknown | tests | Unknown | unknown | [unknown](unknown) | Unknown | unknown | unknown | unknown |



---
Template Copyright [openregulatory.com](https://openregulatory.com). See [template
license](https://openregulatory.com/template-license).

Please don't remove this notice even if you've modified contents of this template.