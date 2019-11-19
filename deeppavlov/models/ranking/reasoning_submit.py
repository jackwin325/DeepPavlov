# Copyright 2017 Neural Networks and Deep Learning lab, MIPT
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from logging import getLogger

import numpy as np

from deeppavlov.core.commands.utils import expand_path
from deeppavlov.core.common.registry import register
from deeppavlov.core.models.component import Component

log = getLogger(__name__)


@register('reasoning_submit')
class ReasoningSubmit(Component):

    def __init__(self,
                 save_path: str,
                 **kwargs) -> None:

        """ Initialize class with given parameters"""

        self.save_path = expand_path(save_path) / "predictions.txt"
        with open('prediction.txt', 'w+') as f:
            f.write('')

    def __call__(self, ids, y_pred):
        question_id = [i[0] for i in ids]
        facts_id = [i[1:] for i in ids]
        orders = np.flip(np.argsort(y_pred, -1), -1)
        ordered_facts = [[facts[i] for i in order] for order, facts in zip(orders, facts_id)]
        submit = [q + '\t' + f for q, facts in zip(question_id, ordered_facts) for f in facts]
        with open('prediction.txt', 'a') as f:
            f.write('\n'.join(submit))
        return y_pred
