/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_memchr.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mafonso <mafonso@student.42porto.com>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/27 20:30:59 by mafonso           #+#    #+#             */
/*   Updated: 2025/10/27 20:47:01 by mafonso          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

void	*ft_memchr(const void *str, int c, size_t n)
{
	size_t				i;
	const unsigned char	*s;
	unsigned char		chr;

	i = 0;
	chr = (unsigned char)c;
	s = str;
	while (i < n)
	{
		if (s[i] == chr)
		{
			return ((void *)(str + i));
		}
		i++;
	}
	return (NULL);
}
