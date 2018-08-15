# Reading Note: Label Ranking by Learning Pairwise Preferences

## Key ideas
- **Ranking by pairwise comparison (RPC)**: reduce the proble of label ranking to several binary classification problems

## Assumptions
- They do not expect the training data to provide full information about the ranking.
- To increase the practical usefulness of this approach, they allow for inconsistencies such as pairwise preferences which are conflicting due to observation errors.

## Some concepts
- Many conventional learning problems such as classification and multi-label classification can be formulated in terms of label preferences
- Approaches to learn from preferences
	- **Learning from object preferences**
	- **Learning from label preferences**
	- **Learning from utility functions**: the challenge is to find a function that is as much as possible in agreement with all constrants.
	- **Learning from preference relations**: the key idea of this approach is to model the individual preferences directly instead of translating them into a utility function. This seems a natural approach since it has already been noted that utility scores are difficult to elicit and observed preferences are usually of the relational type.

## Understanding RPC
- Learning **pair-wise** preference leans **more accurate** theories than the more commonly used **one-against-all** classification method. And it can be shown that pairwise classification is also computationally more efficient than one-against-all class binarization.
- The learned binary preference relation does not necessarily have the typical properties of order relations.
- The overall complexity of paiwise label ranking depends on the average number of preferences that are given for each training example.
- **Disadvantage**
	- A large number of classifiers that have to be stored

## Citation
- E. Hüllermeier, J. Fürnkranz, W. Cheng, and K. Brinker. Label ranking by learning pairwise preferences. Artificial Intelligence, 172(16–17):1897–1916, 2008
	- http://weiweicheng.com/research/papers/cheng-ai08.pdf
