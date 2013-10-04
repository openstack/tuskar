#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
# Copyright 2013 Red Hat
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""Utility/script - fetches heat templates from github"""

import logging
import sys

import os
from oslo.config import cfg

from tuskar.api import config
from tuskar.common import service as tuskar_service
from tuskar.openstack.common import log

CONF = cfg.CONF


def fetch_remote_heat_templates(template_path):
    template_git = CONF.tht_git_repo
    os.system("cd " + template_path + " ; git clone " + template_git)
    #HAX: revert to a specific known-working commit for HK/freeze:
    #uncomment next 3 lines to use:
    # commit_id="0326335160a5977df44ae40d4c81ab8e40833743"
    # os.system("cd " + template_path + "/tripleo-heat-templates; git " +
    #           "reset --hard " + commit_id )


def main():
    tuskar_service.prepare_service(sys.argv)
    LOG = log.getLogger(__name__)
    heat_template_path = CONF.tht_local_dir + "tripleo-heat-templates"
    try:
        if not os.path.exists(heat_template_path):
            LOG.info('Creating directory: ' + heat_template_path)
            os.mkdir(heat_template_path)
        LOG.info("Pulling git repo at " + CONF.tht_git_repo)
        fetch_remote_heat_templates(CONF.tht_local_dir)
    except:
        LOG.error("ERROR problem creating git repo " + CONF.tht_git_repo)
        raise
