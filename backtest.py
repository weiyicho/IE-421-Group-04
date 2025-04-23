class backtest:
    def __init__(self, strategy, data):
        self.strategy = strategy
        self.data = data
        self.results = []

    def run(self):
        for i in range(len(self.data)):
            signal = self.strategy.generate_signal(self.data[i])
            if signal:
                self.results.append(signal)
        return self.results

    def analyze_results(self):
        # Placeholder for analysis logic
        pass