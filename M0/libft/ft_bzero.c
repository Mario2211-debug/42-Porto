/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_bzero.c                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mafonso <mafonso@student.42porto.com>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/27 20:23:40 by mafonso           #+#    #+#             */
/*   Updated: 2025/10/27 20:42:57 by mafonso          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */
#include "libft.h"

void	ft_bzero(void *s, size_t n)
{
	unsigned char	*ft;
	size_t			i;

	ft = (unsigned char *)s;
	i = 0;
	while (i < n)
	{
		ft[i] = 0;
		i++;
	}
}
