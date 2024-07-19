import time
import scrape

if __name__ == "__main__":
    start_time = time.time()
    scrape.scrape()
    print(" %s seconds ---" % (time.time() - start_time))
