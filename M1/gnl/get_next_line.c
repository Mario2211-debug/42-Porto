/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   get_next_line.c                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mafonso <mafonso@student.42porto.com>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/18 20:11:35 by mafonso           #+#    #+#             */
/*   Updated: 2025/12/19 22:53:19 by mafonso          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "get_next_line.h"

char	*ft_strchr(const char *s, int c)
{
	int	i;

	i = 0;
	while (s[i] != '\0')
	{
		if (s[i] == (char)c)
			return ((char *)(s + i));
		i++;
	}
	if ((char)c == '\0')
		return ((char *)(s + i));
	return (NULL);
}

char	*ft_strdup(const char *s)
{
	char	*str;
	int		i;

	i = 0;
	str = malloc(ft_strlen(s) + 1);
	if (!str)
		return (NULL);
	while (s[i] != '\0')
	{
		str[i] = s[i];
		i++;
	}
	str[i] = '\0';
	return (str);
}

void	*free_gnl(char **buffer, char **acc)
{
	free(*acc);
	free(*buffer);
	*acc = NULL;
	return (NULL);
}

char	*alloc_buffer(void)
{
	char	*buffer;

	buffer = malloc(BUFFER_SIZE + 1);
	if (!buffer)
		return (NULL);
	return (buffer);
}

char	*get_next_line(int fd)
{
	char		*newline_pos;
	char		*buffer;
	ssize_t		bytes_read;
	static char	*acc;

	buffer = alloc_buffer();
	while (1)
	{
		if (acc)
		{
			newline_pos = ft_strchr(acc, '\n');
			if (newline_pos)
				return (ft_cut_save(&buffer, &acc, newline_pos));
		}
		bytes_read = read(fd, buffer, BUFFER_SIZE);
		if (bytes_read == -1)
			return (free_gnl(&buffer, &acc));
		if (bytes_read <= 0)
			return (ft_read_line(&buffer, &acc));
		buffer[bytes_read] = '\0';
		acc = str_join(acc, buffer, bytes_read);
		if (!acc)
			return (NULL);
	}
	free(buffer);
}
