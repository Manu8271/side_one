# # import random
# # import string
# # from idlelib import query
# #
# # import requests
# # from bs4 import BeautifulSoup
# #
# # # Define fitness function: Evaluate the relevance of a search query
# # def evaluate_fitness(query, target_keywords):
# #     """
# #     Fitness is calculated as the number of target keywords in the query
# #     :param query:
# #     :param target_keywords:
# #     :return:
# #     """
# #     fitness = 0
# #     for keyword in target_keywords:
# #         if keyword in query:
# #             fitness += 1
# #     return fitness
# #
# # # Perform web search and scrape results
# # def perform_search(query):
# #     """
# #     Simulates an internet search by sending a GET request to a search engine(e.g. google)
# #
# #     :param query:
# #     :return:
# #     """
# #     url = f"https://www.duckduckgo.com/?q={query}"
# #     headers = {"User-Agent": "Mozilla/5.0"}
# #     response = requests.get(url, headers=headers)
# #     soup = BeautifulSoup(response.text, "html.parser")
# #
# #     # Scrape the title of the search results
# #     titles = [title.text for title in soup.find_all("h2")]
# #     return titles
# #
# # # generate the initial population of the random queries
# # def generate_population(size, length):
# #     population = []
# #     for _ in range(size):
# #         quest = ''.join(random.choices(string.ascii_lowercase + " ", k=length))
# #         population.append(query.strip())
# #     return population
# #
# # # Crossover : Combine the parts of two queries to generate offspring
# # def crossover(parent1, parent2):
# #     split = random.randit(1, len(parent1) - 1)
# #     child1 = parent1
#
#
import random
import string






import random
import string
import requests
from bs4 import BeautifulSoup


# Fitness function: Evaluate query relevance
def evaluate_fitness(query, target_keywords):
    fitness = sum(1 for keyword in target_keywords if keyword in query)
    return fitness


# Perform web search and scrape results
def perform_search(query):
    """
    Simulates an internet search by sending a GET request to a search engine .
    """
    url = f"https://www.duckduckgo.com/?q={query}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    # Scrape titles of search results
    titles = [title.text for title in soup.find_all("h2")]
    return titles


# Generate initial population with hints of target keywords
def generate_population(size, target_keywords):
    population = []
    for _ in range(size):
        query = ' '.join(random.choice(target_keywords)[:random.randint(3, len(keyword))] for keyword in target_keywords)
        population.append(query.strip())
    return population

# Crossover: Combine parts of two queries
def crossover(parent1, parent2):
    split = random.randint(1, min(len(parent1), len(parent2)) - 1)
    child1 = parent1[:split] + parent2[split:]
    child2 = parent2[:split] + parent1[split:]
    return child1, child2

# Mutation: Randomly modify the query
def mutate(query, mutation_rate, target_keywords):
    query = list(query)
    for i in range(len(query)):
        if random.random() < mutation_rate:
            query[i] = random.choice(string.ascii_lowercase + " ")  # Add random letters or spaces
    # Add chance to insert target keyword fragments
    if random.random() < mutation_rate:
        keyword = random.choice(target_keywords)
        query.insert(random.randint(0, len(query)), keyword[random.randint(0, len(keyword)-1)])
    return ''.join(query)

# Genetic Algorithm
def genetic_algorithm(target_keywords, population_size=10, generations=50, mutation_rate=0.1):
    population = generate_population(population_size, target_keywords)
    best_query = ""
    best_fitness = 0

    for generation in range(generations):
        # Evaluate fitness for each query
        fitness_scores = [evaluate_fitness(query, target_keywords) for query in population]

        # Track the best query
        max_fitness = max(fitness_scores)
        if max_fitness > best_fitness:
            best_fitness = max_fitness
            best_query = population[fitness_scores.index(max_fitness)]

        print(f"Generation {generation}: Best Query: '{best_query}', Fitness: {best_fitness}")

        if best_fitness == len(target_keywords):  # Perfect match found
            break

        # Selection: Keep top-performing individuals
        sorted_population = [query for _, query in sorted(zip(fitness_scores, population), reverse=True)]
        parents = sorted_population[:population_size // 2]

        # Generate new population with crossover and mutation
        new_population = parents.copy()
        while len(new_population) < population_size:
            parent1, parent2 = random.sample(parents, 2)
            child1, child2 = crossover(parent1, parent2)
            new_population.extend([mutate(child1, mutation_rate, target_keywords),
                                   mutate(child2, mutation_rate, target_keywords)])
        population = new_population[:population_size]

    return best_query

# Example usage
if __name__ == "__main__":
    target_keywords = ["Machine", "Learning", "Algorithms"]
    best_query = genetic_algorithm(target_keywords, population_size=20, generations=100)
    print("\nFinal Optimized Search Query:", best_query)