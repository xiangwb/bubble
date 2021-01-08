from bubble.models import UserSubject, PointRelation, Item


def get_next_item_id(user_id: str, subject_id: str, item_id: str = None, answer: str = None) -> [str, None]:
    user_subject = UserSubject.objects.get(user_id=user_id, subject=subject_id)
    # 存在学习记录
    if user_subject:
        detail = user_subject.detail
        # 如果不提供item，意味着当前初次进入学习
        if item_id is None:
            # 已有学习记录，重新开始学习
            if detail:
                # 第一种情况，
                latest = detail.get('latest')
                latest_item_id = latest.get('item_id')
                answer = latest.get('answer')
                records = latest.get('records')
                # 上次返回item_id，用户没有答，直接退出了
                if answer is None:
                    return latest_item_id
                # 上次回答正确
                if answer:
                    # 新学习一个条目
                    if not records:
                        # 先判断是否需要新学习一个条目，还是复习原先的内容
                        pass
                    else:
                        pass

                # 上次回答错误
                else:
                    # 新学习一个条目
                    if not records:
                        pass
                    else:
                        pass

            # 没有学习记录
            else:
                relation = PointRelation.objects.get(subject_id=subject_id)
                if relation:
                    for index in relation:
                        top_node = relation[index]
                        # 递归
                        while top_node:
                            if 'contains' in top_node:
                                top_node = top_node['contains'][0]
                            else:
                                item = Item.objects.filter(point=top_node['id']).order_by('id').first()
                                if item:
                                    return item.id
                                else:
                                    return None
                    return None
        # 学习中
        else:
            # 存在学习记录
            if detail:
                pass
            # 没有学习记录
            else:
                relation = PointRelation.objects.get(subject_id=subject_id)
                if relation:
                    for index in relation:
                        top_node = relation[index]
                        while top_node:
                            if 'contains' in top_node:
                                top_node = top_node['contains'][0]
                            else:
                                user_subject = UserSubject.objects.get(user_id=user_id, subject_id=subject_id)
                                user_subject.detail = {
                                    'studying': [{"item_id": item_id, "score": 0}],
                                    'mastered': [],
                                    'point_id': top_node['id'],
                                    'point_item_id':[],
                                    'latest': {'item_id': item_id, 'answer': answer,
                                               "records": []},
                                }
                                user_subject.save()
                                return top_node
                    return None
    # 不存在学习记录
    else:
        relation = PointRelation.objects.get(subject_id=subject_id)
        if relation:
            for index in relation:
                top_node = relation[index]
                # 递归
                while top_node:
                    if 'contains' in top_node:
                        top_node = top_node['contains'][0]
                    else:
                        items = Item.objects.filter(point=top_node['id']).order_by('id').only('id')
                        if items:
                            item = items[0]
                            UserSubject.objects.create(
                                user_id=user_id,
                                detail={
                                    'studying': [item.id],
                                    'mastered': [],
                                    'point_id': top_node['id'],
                                    'point_item_ids': items,
                                    'item_id':item.id,
                                    'related_item_ids':[]
                                }
                            )
                            return item.id
                        else:
                            return None
                return None
        else:
            # 不存在该课程,或者课程数据为空
            return None
