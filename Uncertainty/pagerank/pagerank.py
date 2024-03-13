import os
import random
import re
import sys
import numpy
import copy

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    probability_distribution = dict()
    linked_pages = corpus[page]
    for page in corpus:
        probability_distribution[page] = (1-damping_factor)/len(corpus)
    for page in linked_pages:
        probability_distribution[page] += damping_factor/len(linked_pages)
    if len(linked_pages) == 0:
        for page in corpus:
            probability_distribution[page] += damping_factor/len(corpus)
        
    return probability_distribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    sample = random.choice(list(corpus.keys()))
    pagerank = dict()
    for page in corpus:
        pagerank[page] = 0
    pagerank[sample] += 1/n

    for _ in range(n):
        transition = transition_model(corpus, sample, damping_factor)
        sample = numpy.random.choice(list(transition.keys()), p=list(transition.values()))
        pagerank[sample] += 1/n
    return pagerank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pagerank = {}
    N = len(corpus)
    for page in corpus:
        pagerank[page] = 1/N
    
    while True:
        new_pagerank = copy.deepcopy(pagerank)
        done = True
        
        for page in corpus:
            new_rank = (1-damping_factor)/N
            
            for link_page in corpus:
                if page in corpus[link_page]:
                    new_rank += damping_factor*pagerank[link_page]/len(corpus[link_page])
                if len(corpus[link_page]) == 0:
                    new_rank += damping_factor*pagerank[link_page]/N
                        
            if abs(new_rank - pagerank[page]) > 0.001:
                done = False
            new_pagerank[page] = new_rank
        pagerank = new_pagerank
        
        if done:
            break
            
    return pagerank


if __name__ == "__main__":
    main()
