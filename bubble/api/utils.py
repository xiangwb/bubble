from bubble.models import UserSubject, PointRelation, Item


def get_next_item_id(user_id, subject_id, item_id=None, answer=None):
    user_subject = UserSubject.objects.get(user_id=user_id, subject=subject_id)
    if user_subject:
        detail = user_subject.detail
        # 如果不提供item，意味着当前初次进入学习
        if item_id is None:
            if detail:
                pass
            else:
                pass
        else:
            pass
    else:
        detail = {}
        first_relation = PointRelation.objects(subject_id=subject_id, n1_type='subject').order_by('sequence').first() # 该课程下的第一个知识点
        if first_relation:
            n2_id = first_relation.n2_id
            # 该知识点下的第一条目
            relation = PointRelation.objects(subject_id=subject_id, n1_id=n2_id).order_by('sequence').first()
            if relation:
                item_id = relation.n2_id
                # TODO 需要记录到学习状态的信息
                return item_id
            else:
                return None
        else:
            return None

