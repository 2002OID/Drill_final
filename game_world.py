objects = [[] for _ in range(4)]    #시각적 관점의 월드

#충돌관점의 월드
collision_pairs = {} # 'boy:ball' : [boy, ball1] ...
# fill here

def add_object(o, depth = 0):
    objects[depth].append(o)

def add_objects(ol, depth = 0):
    objects[depth] += ol


def update():
    for layer in objects:
        for o in layer:
            o.update()


def render():
    for layer in objects:
        for o in layer:
            o.draw()

# fill here


def remove_collision_object(o):
    for pairs in collision_pairs.values():
        if o in pairs[0]:
            pairs[0].remove(o)
        if o in pairs[1]:
            pairs[1].remove(o)


def remove_object(o):
    for layer in objects:
        if o in layer:
            layer.remove(o)     #시각적 월드에서만 삭제
            remove_collision_object(o)  #충돌그룹에서 삭제
            del o #객체 자체까지 삭제
            return
    raise ValueError('Cannot delete non existing object')


def clear():
    for layer in objects:
        layer.clear()



def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    return True

def add_collision_pair(group, a, b):
    if group not in collision_pairs:
        print(f'new group {group} added')
        collision_pairs[group] = [ [], [] ]
    if a:   #a가 있을떄 == a가 none이 아님
        collision_pairs[group][0].append(a)
    if b:   #b가 있을때 == ㅠ가 none이 아님
        collision_pairs[group][1].append(b)


def handle_collisions():
    #등록된 모든 충돌 상황에대한 검사 및 처리
    for group, pairs in collision_pairs.items():
        for a in pairs[0]:
            for b in pairs[1]:
                if collide(a, b):
                    a.handle_collision(group, b)
                    b.handle_collision(group, a)
