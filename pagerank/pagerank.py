import os
import random
import re
import sys

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
    print("PageRank Results from Iteration")
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
        pages[filename] = set(link for link in pages[filename] if link in pages)

    return pages


def transition_model(corpus, page, d):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    n = len(corpus)
    ret = {}
    for k in corpus.keys():
        ret[k] = (1 - d) / n

    for k in corpus[page]:
        ret[k] += d / len(corpus[page])

    return ret

    raise NotImplementedError


def sample_pagerank(corpus, d, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    s = random.choices(list(corpus.keys()), k=1)
    ret = {}
    for abcd in range(n):
        if s[0] in ret:
            ret[s[0]] += 1 / n
        else:
            ret[s[0]] = 1 / n

        model = transition_model(corpus, s[0], d)
        s = random.choices(list(model.keys()), weights=list(model.values()), k=1)

    return ret

    raise NotImplementedError


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    ranks = dict()

    # set threshold of convergence to be +/- 0.001
    threshold = 0.0005

    # N = no. of pages
    # set the rank of each page to be 1 / N
    N = len(corpus)
    for key in corpus:
        ranks[key] = 1 / N

    # for each page, determine which/how many other pages link to it
    # then, apply the PageRank formula
    # if change (new_rank, old_rank) < threshold update counter
    # if by the end of the loop, counter == N,
    # it means that the change in rank for each page
    # in the corpus was within the threshold
    # so end the loop
    # return rank
    while True:

        count = 0

        for key in corpus:

            new = (1 - damping_factor) / N
            sigma = 0

            for page in corpus:

                if key in corpus[page]:
                    num_links = len(corpus[page])
                    sigma = sigma + ranks[page] / num_links

            sigma = damping_factor * sigma
            new += sigma

            if abs(ranks[key] - new) < threshold:
                count += 1

            ranks[key] = new

        if count == N:
            break

    return ranks
    raise NotImplementedError


if __name__ == "__main__":
    main()
