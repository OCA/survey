To configure the contact generation:

1.  Go to the configured survey.
2.  In the *Contact* section of the *Options* tab, set *Generate
    Contact* on, if you want contacts to be generated from the answers
    to this survey.
3.  If you want the generated to have a parent company, set the option
    *Create Parent Contact* and link the company_name field to a
    question in the survey.
4.  In each question associated with a future new contact, specify the
    corresponding contact field. To do this, go to the 'Options' tab,
    then navigate to the 'Contact' group, and select the 'Contact field'
    field.

To generate a hierarchy of contacts out of a single survey:

1.  A question mapped to the *Name* contact field opens a contact of its
    own. Any other question fills in a field of the contact opened by its
    *Node*.
2.  In such a question, set *Node* to the question opening the contact it
    hangs from. Leave it empty and its answers will belong to the main
    generated contact.
3.  Contacts typed as *Contact* share their address with their parent, so
    set *Contact address type* to *Other address* in the questions opening
    a contact that holds an address of its own.

For instance, this survey generates a company, two of its workcenters
with their own address, and an employee hanging from each workcenter:

| Question             | Contact field | Node                 | Address type  |
|----------------------|---------------|----------------------|---------------|
| Company name         | name          |                      |               |
| Workcenter 1         | name          | Company name         | Other address |
| Workcenter 1 street  | street        | Workcenter 1         |               |
| Workcenter 1 employee| name          | Workcenter 1         |               |
| Workcenter 2         | name          | Company name         | Other address |
| Workcenter 2 street  | street        | Workcenter 2         |               |
| Workcenter 2 employee| name          | Workcenter 2         |               |

A node whose name goes unanswered generates no contact, and whatever hangs
from it hangs from its own node instead.
