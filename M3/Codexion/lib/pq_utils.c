/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   pq_utils.c                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mafonso <mafonso@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/30 19:01:38 by mafonso           #+#    #+#             */
/*   Updated: 2026/08/04 19:47:39 by mafonso          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../libcodexion.h"

/*
Swapp to priority queue nodes.
*/

void	pq_swap(t_pq_node *a, t_pq_node *b)
{
	t_pq_node	tmp;

	tmp = *a;
	*a = *b;
	*b = tmp;
}

/*
** A function that compares two nodes to assist in tie-breaking decisions.
*/

int	pq_higher_priority(t_pq_node *a, t_pq_node *b)
{
	if (a->priority != b->priority)
		return (a->priority < b->priority);
	return (a->tie_breaker > b->tie_breaker);
}

/*
** Moves a node up the heap to restore Mini-heap property.
*/

void	pq_sift_up(t_pqueue *pq, int idx)
{
	int	parent;

	while (idx > 0)
	{
		parent = (idx - 1) / 2;
		if (pq_higher_priority(&pq->nodes[idx], &pq->nodes[parent]))
		{
			pq_swap(&pq->nodes[parent], &pq->nodes[idx]);
			idx = parent;
		}
		else
		{
			break ;
		}
	}
}

/*
** Moves a node down the heap to restore the mini-heap property.
*/

void	pq_sift_down(t_pqueue *pq, int idx)
{
	int	smallest;
	int	right;
	int	left;

	while (1)
	{
		smallest = idx;
		left = 2 * idx + 1;
		right = 2 * idx + 2;
		if (left < pq->size && pq_higher_priority(&pq->nodes[left],
				&pq->nodes[smallest]))
			smallest = left;
		if (right < pq->size && pq_higher_priority(&pq->nodes[right],
				&pq->nodes[smallest]))
			smallest = right;
		if (smallest != idx)
		{
			pq_swap(&pq->nodes[smallest], &pq->nodes[idx]);
			idx = smallest;
		}
		else
			break ;
	}
}

/*
** Returns i if the queue is empty, 0 otherwise.
*/

int	pq_is_empty(t_pqueue *pq)
{
	return (pq->size == 0);
}
