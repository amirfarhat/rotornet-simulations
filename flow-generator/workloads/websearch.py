import random

def websearch_workload_distribution(scale, cdf=None):
    """
    Reproduces the web search workload flow size
    (from the pFabric paper)
    
    Args:
        cdf (None, optional): cdf of flows between
                                0 and 1, otherwise should
                                be None to generate random cdf
    
    Returns:
        int: the flow size depending the given cdf
    
    Raises:
        ValueError: if non-None cdf specified cannot be turned
                    into a float between and clipped to be in [0, 1]
    """
    # random cdf in [0, 1) if no cdf specified
    if cdf is None:
        cdf = random.random()

    # otherwise cdf must be a float between 0 and 1
    else:
        try:
            cdf = float(min(1, max(0, float(cdf))))
        except:
            raise ValueError("Expected numeric cdf value between 0 and 1 but got {}".format(cdf))

    # get flow size depending on the cdf value
    if cdf   <= 0.15:
        size = 6.0

    elif cdf <= 0.2:
        size = random.uniform(6, 13)

    elif cdf <= 0.3:
        size = random.uniform(13, 19)

    elif cdf <= 0.4:
        size = random.uniform(19, 33)

    elif cdf <= 0.53:
        size = random.uniform(33, 53)

    elif cdf <= 0.6:
        size = random.uniform(53, 133)

    elif cdf <= 0.7:
        size = random.uniform(133, 667)

    elif cdf <= 0.8:
        size = random.uniform(667, 1333)

    elif cdf <= 0.9:
        size = random.uniform(1333, 3333)

    elif cdf <= 0.97:
        size = random.uniform(3333, 6667)

    else:
        size = random.uniform(6667, 20000)

    # float range [6, 20 * 1000] --> int range [1, scale]
    return int((((size - 6) / 19994) * (scale - 1)) + 1)