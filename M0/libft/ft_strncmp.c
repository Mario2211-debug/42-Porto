/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strncmp.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mafonso <mafonso@student.42porto.com>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/22 23:50:03 by mafonso           #+#    #+#             */
/*   Updated: 2025/10/23 00:18:14 by mafonso          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

int	ft_strncmp(const char *s1, const char *s2, size_t n)
{
	const unsigned char	*a;
	const unsigned char	*b;
	size_t				i;

	a = (const unsigned char *)s1;
	b = (const unsigned char *)s2;
	i = 0;
	while (i < n && a[i] && b[i] && a[i] == b[i])
	{
		i++;
	}
	if (i == n)
		return (0);
	return (a[i] - b[i]);
}
