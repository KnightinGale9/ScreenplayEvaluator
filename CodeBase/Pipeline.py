class Pipeline:
    def __init__(self, steps):
        self.steps = steps

    def run(self,allEval):

        json_data = {}
        for arg,eval in self.steps:
            if arg or allEval:
                eval.run_evaluator()
                print(", ",end="")
                json_data.update(eval.get_json_data())
        return json_data