You can configure either a new or an existing survey.

#. Go to *Surveys* and choose an existing one or create it.
#. In the *Options* tab, *Sales* group, set *Generate Quotations* on.
#. You can set your preferred sales team for the generated quotations.

Now you'll have to configure the products linked to the questions.

For *Numerical value* questions:

#. In the *Answers* tab choose the linked products.
#. The resulting quotation will have as many items of that products as the user defines.

For *Multiple choice: only one answer*:

#. In the *Answers* tab link multiple products to every given choice.
#. The resulting quotation will have the products linked to the survey user's choice.

For *Multiple choice: multiple answers allowed*:

#. In the *Answers* tab link products to every given choice.
#. The resulting quotation will have the products linked to the survey user's choices.
#. By default a unit of product will be added per answer to the quotation. If you want
   to set a variable choice, you can link a numeric question that will act as multiplier.

When the survey is submited an internal message is generated in the resulting quotation
with a link to the user answers. Optionally, you can configure some of the questions so
their input values are shown in such message. This way it can be easier to track some
relevant infos concerning the request. To do so:

#. In the *Options* tab of the questions go to the *Sales* section.
#. Set *Show in sale order comment* on if you want those answers on the internal
   notification.

If you want to use a quotation template you can choose it from the options: *Sale Order Template*.

You can also configure the survey to send the quotation to the customer by mail. When doing
so, you can choose a mail template or use the default one.

If you want to fill sale fields from the answers:

#. In the *Options* tab of the questions go to the *Sales* section.
#. Set *Sale the sale field* you want to fill with the given answer.
