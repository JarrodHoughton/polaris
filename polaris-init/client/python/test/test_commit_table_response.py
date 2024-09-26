#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#
# coding: utf-8

"""
    Apache Iceberg REST Catalog API

    Defines the specification for the first version of the REST Catalog API. Implementations should ideally support both Iceberg table specs v1 and v2, with priority given to v2.

    The version of the OpenAPI document: 0.0.1
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from polaris.catalog.models.commit_table_response import CommitTableResponse

class TestCommitTableResponse(unittest.TestCase):
    """CommitTableResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> CommitTableResponse:
        """Test CommitTableResponse
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `CommitTableResponse`
        """
        model = CommitTableResponse()
        if include_optional:
            return CommitTableResponse(
                metadata_location = '',
                metadata = polaris.catalog.models.table_metadata.TableMetadata(
                    format_version = 1, 
                    table_uuid = '', 
                    location = '', 
                    last_updated_ms = 56, 
                    properties = {
                        'key' : ''
                        }, 
                    schemas = [
                        null
                        ], 
                    current_schema_id = 56, 
                    last_column_id = 56, 
                    partition_specs = [
                        polaris.catalog.models.partition_spec.PartitionSpec(
                            spec_id = 56, 
                            fields = [
                                polaris.catalog.models.partition_field.PartitionField(
                                    field_id = 56, 
                                    source_id = 56, 
                                    name = '', 
                                    transform = '["identity","year","month","day","hour","bucket[256]","truncate[16]"]', )
                                ], )
                        ], 
                    default_spec_id = 56, 
                    last_partition_id = 56, 
                    sort_orders = [
                        polaris.catalog.models.sort_order.SortOrder(
                            order_id = 56, 
                            fields = [
                                polaris.catalog.models.sort_field.SortField(
                                    source_id = 56, 
                                    transform = '["identity","year","month","day","hour","bucket[256]","truncate[16]"]', 
                                    direction = 'asc', 
                                    null_order = 'nulls-first', )
                                ], )
                        ], 
                    default_sort_order_id = 56, 
                    snapshots = [
                        polaris.catalog.models.snapshot.Snapshot(
                            snapshot_id = 56, 
                            parent_snapshot_id = 56, 
                            sequence_number = 56, 
                            timestamp_ms = 56, 
                            manifest_list = '', 
                            summary = {
                                'key' : ''
                                }, 
                            schema_id = 56, )
                        ], 
                    refs = {
                        'key' : polaris.catalog.models.snapshot_reference.SnapshotReference(
                            type = 'tag', 
                            snapshot_id = 56, 
                            max_ref_age_ms = 56, 
                            max_snapshot_age_ms = 56, 
                            min_snapshots_to_keep = 56, )
                        }, 
                    current_snapshot_id = 56, 
                    last_sequence_number = 56, 
                    snapshot_log = [
                        polaris.catalog.models.snapshot_log_inner.SnapshotLog_inner(
                            snapshot_id = 56, 
                            timestamp_ms = 56, )
                        ], 
                    metadata_log = [
                        polaris.catalog.models.metadata_log_inner.MetadataLog_inner(
                            metadata_file = '', 
                            timestamp_ms = 56, )
                        ], 
                    statistics_files = [
                        polaris.catalog.models.statistics_file.StatisticsFile(
                            snapshot_id = 56, 
                            statistics_path = '', 
                            file_size_in_bytes = 56, 
                            file_footer_size_in_bytes = 56, 
                            blob_metadata = [
                                polaris.catalog.models.blob_metadata.BlobMetadata(
                                    type = '', 
                                    snapshot_id = 56, 
                                    sequence_number = 56, 
                                    fields = [
                                        56
                                        ], )
                                ], )
                        ], 
                    partition_statistics_files = [
                        polaris.catalog.models.partition_statistics_file.PartitionStatisticsFile(
                            snapshot_id = 56, 
                            statistics_path = '', 
                            file_size_in_bytes = 56, )
                        ], )
            )
        else:
            return CommitTableResponse(
                metadata_location = '',
                metadata = polaris.catalog.models.table_metadata.TableMetadata(
                    format_version = 1, 
                    table_uuid = '', 
                    location = '', 
                    last_updated_ms = 56, 
                    properties = {
                        'key' : ''
                        }, 
                    schemas = [
                        null
                        ], 
                    current_schema_id = 56, 
                    last_column_id = 56, 
                    partition_specs = [
                        polaris.catalog.models.partition_spec.PartitionSpec(
                            spec_id = 56, 
                            fields = [
                                polaris.catalog.models.partition_field.PartitionField(
                                    field_id = 56, 
                                    source_id = 56, 
                                    name = '', 
                                    transform = '["identity","year","month","day","hour","bucket[256]","truncate[16]"]', )
                                ], )
                        ], 
                    default_spec_id = 56, 
                    last_partition_id = 56, 
                    sort_orders = [
                        polaris.catalog.models.sort_order.SortOrder(
                            order_id = 56, 
                            fields = [
                                polaris.catalog.models.sort_field.SortField(
                                    source_id = 56, 
                                    transform = '["identity","year","month","day","hour","bucket[256]","truncate[16]"]', 
                                    direction = 'asc', 
                                    null_order = 'nulls-first', )
                                ], )
                        ], 
                    default_sort_order_id = 56, 
                    snapshots = [
                        polaris.catalog.models.snapshot.Snapshot(
                            snapshot_id = 56, 
                            parent_snapshot_id = 56, 
                            sequence_number = 56, 
                            timestamp_ms = 56, 
                            manifest_list = '', 
                            summary = {
                                'key' : ''
                                }, 
                            schema_id = 56, )
                        ], 
                    refs = {
                        'key' : polaris.catalog.models.snapshot_reference.SnapshotReference(
                            type = 'tag', 
                            snapshot_id = 56, 
                            max_ref_age_ms = 56, 
                            max_snapshot_age_ms = 56, 
                            min_snapshots_to_keep = 56, )
                        }, 
                    current_snapshot_id = 56, 
                    last_sequence_number = 56, 
                    snapshot_log = [
                        polaris.catalog.models.snapshot_log_inner.SnapshotLog_inner(
                            snapshot_id = 56, 
                            timestamp_ms = 56, )
                        ], 
                    metadata_log = [
                        polaris.catalog.models.metadata_log_inner.MetadataLog_inner(
                            metadata_file = '', 
                            timestamp_ms = 56, )
                        ], 
                    statistics_files = [
                        polaris.catalog.models.statistics_file.StatisticsFile(
                            snapshot_id = 56, 
                            statistics_path = '', 
                            file_size_in_bytes = 56, 
                            file_footer_size_in_bytes = 56, 
                            blob_metadata = [
                                polaris.catalog.models.blob_metadata.BlobMetadata(
                                    type = '', 
                                    snapshot_id = 56, 
                                    sequence_number = 56, 
                                    fields = [
                                        56
                                        ], )
                                ], )
                        ], 
                    partition_statistics_files = [
                        polaris.catalog.models.partition_statistics_file.PartitionStatisticsFile(
                            snapshot_id = 56, 
                            statistics_path = '', 
                            file_size_in_bytes = 56, )
                        ], ),
        )
        """

    def testCommitTableResponse(self):
        """Test CommitTableResponse"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
