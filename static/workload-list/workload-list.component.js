'use strict';

// Register `workloadList` component, along with its associated controller and template
angular.
  module('workloadList').
  component('workloadList', {
    templateUrl: 'workload-list/workload-list.template.html',
    controller: function WorkloadListController($http, $interval) {
      var self = this;
      self.status = 'loading';
      self.sort = "max_delay_time";
      var defaultDelayTime = 600;
      var defaultDelayTimeForTest = 120;

      function initWorkloadStatus($http) {
        $http.get('/workload/status').then(function(response) {
          var workloadStatus = response.data;
          self.hostInst = workloadStatus.hostInst
          self.instQnum = workloadStatus.instQnum
          /*
          var selectedInstances = {};
          var partnerDetailExpanded = {};
          for (var i in workloadStatus) {
            selectedInstances[workloadStatus[i].hostname] = workloadStatus[i].instance_list[0];
            for (var instance in workloadStatus[i].instances_data) {
              partnerDetailExpanded[workloadStatus[i].hostname+instance] = false;
              for (var j in  workloadStatus[i].instances_data[instance]) {
                partnerDetailExpanded[workloadStatus[i].hostname+instance+workloadStatus[i].instances_data[instance][j].partner_id]=false;
              }
            }
          }
          self.workloadStatus = workloadStatus;
          self.selectedInstances = selectedInstances;
          self.partnerDetailExpanded = partnerDetailExpanded;
          */
          self.status = 'ready';
        }, function(response) {
          self.status = 'error';
        }).finally(function() {
        });
      };
      initWorkloadStatus($http);

      function getWorkloadStatus($http) {
        $http.get('/workload/status').then(function(response) {
          self.workloadStatus = response.data;
        }, function(response) {
          self.status = 'error';
        }).finally(function() {
        });
      };
      var getWorkloadStatusPolling = getWorkloadStatus.bind(self, $http);
      $interval(getWorkloadStatusPolling, 60000);

      self.showStatus = function showStatus(hostname, instance) {
        self.selectedInstances[hostname] = instance;
      };

      self.isOldData = function isOldData(partnerData) {
        if (partnerData.partner_id != "DUMMY QUEUE") {
          return partnerData.max_delay_time>defaultDelayTime;
        } else {
          return partnerData.max_delay_time>defaultDelayTimeForTest;
        }
      };

      self.setSort = function setSort(option) {
        if (self.sort == option) {
          self.sort = "-" + option;
        } else if (self.sort == "-" + option) {
          self.sort = option;
        } else {
          self.sort = option;
        }
      };

      self.expandAll = function expandAll(hostname, instance, instanceData) {
        self.partnerDetailExpanded[hostname+instance] = !self.partnerDetailExpanded[hostname+instance];
        for (var i in  instanceData) {
          self.partnerDetailExpanded[hostname+instance+instanceData[i].partner_id] = self.partnerDetailExpanded[hostname+instance];
        }
      };

      self.expand = function expand(hostname, instance, partner_id) {
        self.partnerDetailExpanded[hostname+instance+partner_id] = !self.partnerDetailExpanded[hostname+instance+partner_id];
      };

      self.delayedQueueExistsOnInstance = function delayedQueueExistsOnInstance(instance_data) {
        var maxDelayedTimeForThisInstance = 0;
        for (var i in instance_data) {
          maxDelayedTimeForThisInstance = Math.max(maxDelayedTimeForThisInstance, instance_data[i].max_delay_time);
        }
        return maxDelayedTimeForThisInstance>defaultDelayTime;
      };
    }
  });
