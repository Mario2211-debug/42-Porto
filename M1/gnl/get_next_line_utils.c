/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   get_next_line_utils.c                              :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mafonso <mafonso@student.42porto.com>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/18 20:07:26 by mafonso           #+#    #+#             */
/*   Updated: 2025/12/19 22:53:56 by mafonso          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "get_next_line.h"

int	ft_strlen(const char *str)
{
	int	i;

	i = 0;
	while (str[i])
	{
		i++;
	}
	return (i);
}

char	*ft_read_line(char **buffer, char **acc)
{
	char	*str;

	free(*buffer);
	if (*acc && **acc)
	{
		str = *acc;
		*acc = NULL;
		return (str);
	}
	free(*acc);
	*acc = NULL;
	return (NULL);
}

char	*ft_cut_save(char **buffer, char **acc, char *newline_pos)
{
	size_t	line_len;
	char	*line;
	char	*rest;

	free(*buffer);
	line_len = newline_pos - *acc + 1;
	line = malloc(line_len + 1);
	if (!line)
		return (NULL);
	ft_memcpy(line, *acc, line_len);
	line[line_len] = '\0';
	rest = ft_strdup(*acc + line_len);
	free(*acc);
	*acc = rest;
	return (line);
}

void	*ft_memcpy(void *dst, const void *src, size_t num)
{
	size_t			i;
	unsigned char	*d;
	unsigned char	*s;

	i = 0;
	d = (unsigned char *)dst;
	s = (unsigned char *)src;
	while (i < num)
	{
		d[i] = s[i];
		i++;
	}
	return (dst);
}

char	*str_join(char *s1, char *s2, size_t len2)
{
	size_t	len1;
	char	*new_str;

	if (s1)
		len1 = ft_strlen(s1);
	else
		len1 = 0;
	new_str = malloc(len1 + len2 + 1);
	if (!new_str)
		return (NULL);
	if (s1)
		ft_memcpy(new_str, s1, len1);
	ft_memcpy(new_str + len1, s2, len2);
	new_str[len1 + len2] = '\0';
	free(s1);
	return (new_str);
}
