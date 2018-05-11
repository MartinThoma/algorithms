#!/usr/bin/env python

"""Print OpenAI Gym Environment data."""

import gym
from gym import envs
envids = [spec.id for spec in envs.registry.all()]
print('<table class="table">')
print('<tr>')
print('<th>#</th>')
print('<th>Environment</th>')
print('<th>Observation Space</th>')
print('<th>Action Space</th>')
print('<th>Reward Range</th>')
# print('<th>rThresh</th>')
print('</tr>')
for i, envid in enumerate(sorted(envids), start=1):
    try:
        env = gym.make(envid)
        observations = env.observation_space
        actions = env.action_space
        reward = env.reward_range
        rThresh = env.r_thresh
    except:
        observations = 'Error'
        actions = 'Error'
        reward = 'Error'
        rThresh = 'Error'
    print('<tr><td id="env-{i}">{i}</td>'
          '<td><a href="https://gym.openai.com/envs/{envid}/" id="{envid}">'
          '{envid}</a></td>'
          '<td>{observations}</td>'
          '<td>{actions}</td>'
          '<td>{reward}</td>'
          # '<td>{rThresh}</td>'
          '</tr>'
          .format(i=i,
                  envid=envid,
                  observations=str(observations),
                  actions=str(actions),
                  reward=reward,
                  # rThresh=rThresh
                  ))
print('</table>')
