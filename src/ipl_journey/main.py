from .analysis import summarize

def run():
    print("IPL Journey demo starting...")
    s = summarize([1,2,3,4])
    print("Summary:", s)

if __name__ == '__main__':
    run()
