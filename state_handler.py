from collections import deque
import copy

class StateHandler:
    def __init__(self):
        self._states = deque([])
        self.max_size = 4
        
    def __getitem__(self, index):
        return self._states[index]
    
    def __bool__(self):
        return bool(self._states)
    
    def clear(self):
        self._states.clear()
    
    def save_state(self, obj):
        if len(self._states) == self.max_size:
            self._states.pop()
        obj_copy = copy.deepcopy(obj) 
        self._states.appendleft(obj_copy)
        
    def take_previous_state(self):
        if not self:
            raise ValueError("Nie możesz więcej się cofnąć")
        return self._states.popleft()
        
    
