# -*- encoding: utf-8 -*-
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from datetime import datetime

from mock import Mock

from tuskar.storage.models import StoredFile
from tuskar.storage.stores import _BaseStore
from tuskar.storage.stores import _NamedStore
from tuskar.storage.stores import _VersionedStore
from tuskar.storage.stores import DeploymentPlanStore
from tuskar.storage.stores import EnvironmentFileStore
from tuskar.storage.stores import RoleStore
from tuskar.storage.stores import TemplateStore
from tuskar.tests.base import TestCase


class BaseStoreTests(TestCase):

    def setUp(self):

        self.driver = Mock()
        self.store = _BaseStore(self.driver)

    def test_create(self):
        self.store.create("My contents")
        self.driver.create.assert_called_once_with(
            self.store, None, "My contents")

    def test_update(self):
        uuid = "d131dd02c5e6eec4"
        contents = "Stored contents"
        self.store.update(uuid, contents)
        self.driver.update.assert_called_once_with(
            self.store, uuid, None, contents)

    def test_retrieve(self):
        uuid = "d131dd02c5e6eec5"
        self.store.retrieve(uuid)
        self.driver.retrieve.assert_called_once_with(self.store, uuid)

    def test_delete(self):
        uuid = "d131dd02c5e6eec6"
        self.store.delete(uuid)
        self.driver.delete.assert_called_once_with(self.store, uuid)

    def test_list(self):
        self.store.list()
        self.driver.list.assert_called_once_with(self.store)


class NamedStoreTests(TestCase):

    def setUp(self):

        self.driver = Mock()
        self.store = _NamedStore(self.driver)

    def test_create(self):
        name = "Object name"
        self.store.create(name, "My contents")
        self.driver.create.assert_called_once_with(
            self.store, name, "My contents")

    def test_update(self):
        name = "Object name"
        uuid = "d131dd02c5e6eec4"
        contents = "Stored contents"
        self.store.update(uuid, name, contents)
        self.driver.update.assert_called_once_with(
            self.store, uuid, name, contents)

    def test_retrieve(self):
        uuid = "d131dd02c5e6eec5"
        self.store.retrieve(uuid)
        self.driver.retrieve.assert_called_once_with(self.store, uuid)

    def test_delete(self):
        uuid = "d131dd02c5e6eec6"
        self.store.delete(uuid)
        self.driver.delete.assert_called_once_with(self.store, uuid)

    def test_list(self):
        self.store.list()
        self.driver.list.assert_called_once_with(self.store)

    def test_retrieve_by_name(self):
        name = "Object name"
        self.store.retrieve_by_name(name)
        self.driver.retrieve_by_name.assert_called_once_with(self.store, name)


class VersionedStoreTests(TestCase):

    def setUp(self):

        self.driver = Mock()
        self.store = _VersionedStore(self.driver)

    def test_create(self):
        name = "Object name"
        self.store.create(name, "My contents")
        self.driver.create.assert_called_once_with(
            self.store, name, "My contents")

    def test_update(self):
        name = "Object name"
        uuid = "d131dd02c5e6eec4"
        contents = "Stored contents"
        self.store.update(uuid, name, contents)
        self.driver.update.assert_called_once_with(
            self.store, uuid, name, contents)

    def test_retrieve(self):
        uuid = "d131dd02c5e6eec5"
        self.store.retrieve(uuid)
        self.driver.retrieve.assert_called_once_with(self.store, uuid)

    def test_delete(self):
        uuid = "d131dd02c5e6eec6"
        self.store.delete(uuid)
        self.driver.delete.assert_called_once_with(self.store, uuid)

    def test_list(self):
        self.store.list()
        self.driver.list.assert_called_once_with(self.store, only_latest=False)

        self.driver.list.reset_mock()

        self.store.list(only_latest=True)
        self.driver.list.assert_called_once_with(self.store, only_latest=True)

    def test_retrieve_by_name(self):
        name = "Object name"
        version = 1
        self.store.retrieve_by_name(name, version)
        self.driver.retrieve_by_name.assert_called_once_with(
            self.store, name, version)


class TemplateStoreTests(TestCase):

    def setUp(self):

        self.driver = Mock()
        self.store = TemplateStore(self.driver)

    def test_create(self):
        name = "template name"
        contents = "template contents"
        self.store.create(name, contents)
        self.driver.create.assert_called_once_with(self.store, name, contents)


class RoleStoreTests(TestCase):

    def setUp(self):

        self.driver = Mock()
        self.store = RoleStore(self.driver)

    def test_create(self):
        name = "role name"
        contents = "role contents"
        self.store.create(name, contents)
        self.driver.create.assert_called_once_with(self.store, name, contents)


class EnvironmentFileTests(TestCase):

    def setUp(self):

        self.driver = Mock()
        self.store = EnvironmentFileStore(self.driver)

    def test_create(self):
        contents = "environment contents"
        self.store.create(contents)
        self.driver.create.assert_called_once_with(self.store, None, contents)


class DeploymentPlanTests(TestCase):

    def setUp(self):

        self.driver = Mock()
        self.template_store = Mock()
        self.environment_store = Mock()

        self.store = DeploymentPlanStore(
            driver=self.driver,
            template_store=self.template_store,
            environment_store=self.environment_store
        )

    def _stored_file(self, name, contents):

        dt = datetime.now()

        return StoredFile(
            uuid="Plan UUID",
            contents=contents,
            store="deployment_plan",
            name=name,
            created_at=dt,
            updated_at=None,
            version=1,
        )

    def test_create(self):

        name = "deployment_plan name"
        contents = ('{"master_template_uuid": "Template UUID", '
                    '"environment_file_uuid": "Environment UUID"}')

        self.driver.create.return_value = self._stored_file(name, contents)

        result = self.store.create(name, 'Template UUID', 'Environment UUID')
        self.driver.create.assert_called_once_with(self.store, name, contents)

        self.assertEqual(result.name, name)

        self.template_store.retrieve.assert_called_once_with('Template UUID')
        self.environment_store.retrieve.assert_called_once_with(
            'Environment UUID')

    def test_create_no_template(self):

        name = "deployment_plan name"
        contents = ('{"master_template_uuid": "UUID1", '
                    '"environment_file_uuid": "Environment UUID"}')

        self.driver.create.return_value = self._stored_file(name, contents)
        self.template_store.create.return_value = Mock(uuid="UUID1")

        result = self.store.create(name, environment_uuid='Environment UUID')

        self.template_store.create.assert_called_once_with(
            'deployment_plan name', '')
        self.assertItemsEqual(self.environment_store.create.call_args_list, [])

        self.driver.create.assert_called_once_with(self.store, name, contents)

        self.assertEqual(result.name, name)
        self.template_store.retrieve.assert_called_once_with('UUID1')
        self.environment_store.retrieve.assert_called_once_with(
            'Environment UUID')

    def test_create_no_environment(self):

        name = "deployment_plan name"
        contents = ('{"master_template_uuid": "Template UUID", '
                    '"environment_file_uuid": "UUID2"}')

        self.driver.create.return_value = self._stored_file(name, contents)
        self.environment_store.create.return_value = Mock(uuid="UUID2")

        result = self.store.create(name, master_template_uuid='Template UUID')

        self.environment_store.create.assert_called_once_with('')
        self.assertItemsEqual(self.template_store.create.call_args_list, [])

        self.driver.create.assert_called_once_with(self.store, name, contents)

        self.assertEqual(result.name, name)
        self.template_store.retrieve.assert_called_once_with('Template UUID')
        self.environment_store.retrieve.assert_called_once_with(
            'UUID2')
