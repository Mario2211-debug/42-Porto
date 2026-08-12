/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   libcodexion.h                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mafonso <mafonso@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/30 17:19:27 by mafonso           #+#    #+#             */
/*   Updated: 2026/08/04 18:19:20 by mafonso          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef LIBCODEXION_H
# define LIBCODEXION_H

# include <limits.h>
# include <pthread.h>
# include <stdio.h>
# include <stdlib.h>
# include <string.h>
# include <sys/time.h>
# include <unistd.h>

/*
** Schedule types
*/

# define SCHED_EDF_MODE 1
# define SCHED_FIFO_MODE 0

/*
** Coder states
*/
# define ETIMEDOUT 5
# define STATE_THINKING 0
# define STATE_TAKE_DONGLE 1
# define STATE_COMPILING 2
# define STATE_DEBUGGING 3
# define STATE_REFACTORING 4
# define STATE_BURNED_OUT 5

/*
** Foward declarations
*/
typedef struct s_data		t_data;
typedef struct s_coder		t_coder;
typedef struct s_dongle		t_dongle;
typedef struct s_pqueue		t_pqueue;
typedef struct s_pq_node	t_pq_node;

/*
** Priority queue node for schedule
*/

struct						s_pq_node
{
	int						coder_id;
	long					priority;
	long long				tie_breaker;
};

/*
** Mini heap priority queue
*/
struct						s_pqueue
{
	t_pq_node				*nodes;
	int						size;
	int						capacity;
	pthread_mutex_t			lock;
};

/*
** Dongle structure (shared resources)
*/
struct						s_dongle
{
	int						id;
	int						is_taken;
	long					avaliable_at;
	pthread_mutex_t			dongle_lock;
	pthread_cond_t			cond;
	t_pqueue				wait_queue;
	t_data					*data;
};

/*
** Coder structure (one per thread)
*/

struct						s_coder
{
	int						id;
	int						compiles_done;
	long					last_compile_start;
	long					deadline;
	int						status;

	pthread_mutex_t			coder_lock;
	pthread_t				thread_id;
	t_data					*data;
	t_dongle				*left_dongle;
	t_dongle				*right_dongle;
};

/*
** Main simulation data
*/

struct						s_data
{
	int						n_coders;
	long					tt_butnout;
	long					tt_compile;
	long					tt_debug;
	long					tt_refractor;
	int						compiles_required;
	long					dongle_cooldown;
	int						scheduler;
	long					start_time;
	int						sim_over;
	int						someone_burned;
	pthread_mutex_t			log_mutex;
	pthread_mutex_t			sim_mutex;
	t_dongle				*dongles;
	t_coder					*coders;
	pthread_t				monitor_thread;
};

/*
** Time utilities
*/
long						get_time_ms(void);
long						get_elapsed_ms(t_data *data);
void						precise_usleep(long duration_ms, t_data *data);
struct timespec				get_timeout(long ms);

/*
** Coder Utilities
*/
void						acquire_dongles(t_coder *coder);
void						release_dongles(t_coder *coder);
void						do_compile(t_coder *coder);
void						do_debug(t_coder *coder);
void						do_refractor(t_coder *coder);

/*
** Logging
*/
void						log_action(t_data *data, int coder_id,
								const char *action);

/*
** Simulation control
*/
int							is_sim_over(t_data *data);
void						set_sim_over(t_data *data);

/*
** Initialization
*/
int							parse_args(t_data *data, int argc, char **argv);
int							init_simulation(t_data *data);
void						cleanup_simulation(t_data *t_data);

/*
** Dongle managment
*/
void						init_dongle(t_dongle *dongle, int id, t_data *data);
void						destroy_dongle(t_dongle *dongle);
void						take_dongle(t_coder *coder, t_dongle *dongle);
void						release_dongle(t_coder *coder, t_dongle *dongle);

/*
** Priority queue
*/
int							pq_init(t_pqueue *pq, int capacity);
void						pq_destroy(t_pqueue *pq);
void						pq_push(t_pqueue *pq, int coder_id, long priority);
int							pq_pop(t_pqueue *pq);
int							pq_peek(t_pqueue *pq);

/*
**Priority Queue Utilities
*/
int							pq_is_empty(t_pqueue *pq);
void						pq_swap(t_pq_node *a, t_pq_node *b);
int							pq_higher_priority(t_pq_node *a, t_pq_node *b);
void						pq_sift_up(t_pqueue *pq, int idx);
void						pq_sift_down(t_pqueue *pq, int idx);

/*
** Coder Thread
*/
void						*coder_routine(void *arg);

/*
** Monitor thread
*/

void						*monitor_routine(void *args);

#endif