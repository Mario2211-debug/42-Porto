/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_calloc.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mafonso <mafonso@student.42porto.com>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/11 17:24:25 by mafonso           #+#    #+#             */
/*   Updated: 2025/11/13 17:59:41 by mafonso          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

void	*ft_calloc(size_t nmemb, size_t size)
{
	unsigned char	*ptr;
	size_t			i;
	void			*arr;

	if (size != 0 && nmemb > SIZE_MAX / size)
		return (NULL);
	if (nmemb == 0 || size == 0)
	{
		nmemb = 1;
		size = 1;
	}
	arr = malloc(nmemb * size);
	if (!arr)
		return (NULL);
	ptr = (unsigned char *)arr;
	i = 0;
	while (i < nmemb * size)
	{
		ptr[i] = 0;
		i++;
	}
	return (arr);
}
