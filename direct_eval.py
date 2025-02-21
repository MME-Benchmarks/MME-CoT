
import string
import copy as cp

def get_choices(data):
    choices = {}
    for k in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K']:
        if k in data and data[k] is not None and data[k].strip() not in ['nan', '']:
            choices[k] = data[k]
    return choices

def can_infer_option(answer, choices):
    def count_choice(splits, choices, prefix='', suffix=''):
        cnt = 0
        for c in choices:
            if prefix + c + suffix in splits:
                cnt += 1
        return cnt

    answer_mod = cp.copy(answer)
    chars = '.()[],:;!*#{}'
    for c in chars:
        answer_mod = answer_mod.replace(c, ' ')

    splits = [x.strip() for x in answer_mod.split()]
    count = count_choice(splits, choices)

    if count == 1:
        for ch in choices:
            if ch in splits:
                return ch
    return False


def can_infer_text(answer, choices):
    answer = answer.lower()
    assert isinstance(choices, dict)
    for k in choices:
        assert k in string.ascii_uppercase
        choices[k] = str(choices[k]).lower()
    cands = []
    for k in choices:
        if choices[k] in answer:
            cands.append(k)
    if len(cands) == 1:
        return cands[0]
    return False


def can_infer(answer, choices):
    answer = str(answer)
    copt = can_infer_option(answer, choices)
    return copt if copt else can_infer_text(answer, choices)


def extract_answer_from_item(c, cot_gt_item):
    try:
        response = c['prediction']
        assert response != None
    except Exception as e:
        print(f"No prediction: {c}")
        return 'Z'

    gt_answer = c['answer']
    # preprocess
    if len(response.split()) > 10:
        final_answer_patterns = ["Answer:", "Final answer", "final answer", "Final Answer", "the answer is", "The answer is", "correct answer", "Correct answer", "Correct Answer", "<CONCLUSION>"]
        for pattern in final_answer_patterns:
            if pattern in response:
                response = response.split(pattern)[-1].strip()
                break
        else:
            return None 
    ret = False
    # if multi choice
    if len(gt_answer) == 1 and gt_answer.isupper():
        choices = get_choices(cot_gt_item)
        ret = can_infer(response, choices)
    # if cannot directly infer, try to shorten the answer
    if not ret:
        # match \boxed{}
        if 'oxed{' in response:
            response = response.split('oxed{')[-1]
            response = r'\boxed{' + response
        response = response.lstrip(":").strip()
        ret = response
    return ret