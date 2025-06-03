## To use the module with single select or multi-select answers:

    - go to survey app > create a template
    - create a question of type single select or multi-select
    - add a selective answer and write the answer including the field value like:

        - "My name is {{object.name}}" or just {{object.name}}

## To use the module with text or multi-text answers:

    - go to survey app > create a template
    - create a question of type single text or multi-text
    - go to options tab > add a value to suggested_prefilled_answer or suggested_prefilled_answer_multi
    - The dynamic prefilled answer can be like "My name is {{object.name}}" or just {{object.name}}
    - For multi-text answer you can add answer in muti-lines text

Survey participant can still modify the prefilled answers the way they like during the
survey.
