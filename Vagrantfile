# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|

  ####################
  ## Site 1 Router  ##
  ####################
  config.vm.define 'site1router' do |router|
    router.vm.box = 'briantsaunders/frrouting-stable-7.0'
    router.vm.provider "virtualbox" do |settings|
      settings.customize ["modifyvm", :id, "--nicpromisc3", "allow-all"]
    end
    router.vm.hostname = 'site1router'
    router.vm.synced_folder '.',
      '/vagrant',
      disabled: false
    router.vm.network 'private_network',
      auto_config: true,
      nic_type: '82540EM',
      virtualbox__intnet: 'isp_a',
      ip: '192.168.0.2',
      netmask: '255.255.255.254'
    router.vm.network 'private_network',
      auto_config: false,
      nic_type: '82540EM',
      virtualbox__intnet: 'lan_1'
  end

  ####################
  ## Site 1 Server  ##
  ####################
  config.vm.define 'site1server' do |server|
    server.vm.box = 'ubuntu/bionic64'
    server.vm.provider "virtualbox" do |settings|
      settings.cpus = 1
      settings.memory = 512
    end
    server.vm.hostname = 'site1server'
    server.vm.synced_folder '.',
      '/vagrant',
      disabled: false
    server.vm.network 'private_network',
      auto_config: true,
      nic_type: '82540EM',
      virtualbox__intnet: 'lan_1',
      ip: '172.16.0.10',
      netmask: '255.255.255.0'
  end

  ####################
  ## ISP Router  #####
  ####################
  config.vm.define 'isp' do |router|
    router.vm.box = 'briantsaunders/frrouting-stable-7.0'
    router.vm.hostname = 'isp'
    router.vm.synced_folder '.',
      '/vagrant',
      disabled: false
    router.vm.network 'private_network',
      auto_config: true,
      nic_type: '82540EM',
      virtualbox__intnet: 'isp_a',
      ip: '192.168.0.3',
      netmask: '255.255.255.254'
    router.vm.network 'private_network',
      auto_config: true,
      nic_type: '82540EM',
      virtualbox__intnet: 'isp_b',
      ip: '192.168.0.4',
      netmask: '255.255.255.254'
  end

  ####################
  ## Site 2 Router  ##
  ####################
  config.vm.define 'site2router' do |router|
    router.vm.box = 'briantsaunders/frrouting-stable-7.0'
    router.vm.provider "virtualbox" do |settings|
      settings.customize ["modifyvm", :id, "--nicpromisc3", "allow-all"]
    end
    router.vm.hostname = 'site2router'
    router.vm.synced_folder '.',
      '/vagrant',
      disabled: false
    router.vm.network 'private_network',
      auto_config: true,
      nic_type: '82540EM',
      virtualbox__intnet: 'isp_b',
      ip: '192.168.0.5',
      netmask: '255.255.255.254'
    router.vm.network 'private_network',
      auto_config: false,
      nic_type: '82540EM',
      virtualbox__intnet: 'lan_3'
  end

  ####################
  ## Site 2 Server  ##
  ####################
  config.vm.define 'site2server' do |server|
    server.vm.box = 'ubuntu/bionic64'
    server.vm.provider "virtualbox" do |settings|
      settings.cpus = 1
      settings.memory = 512
    end
    server.vm.hostname = 'site2server'
    server.vm.synced_folder '.',
      '/vagrant',
      disabled: false
    server.vm.network 'private_network',
      auto_config: true,
      nic_type: '82540EM',
      virtualbox__intnet: 'lan_3',
      ip: '172.16.0.11',
      netmask: '255.255.255.0'
  end

  ####################
  ## Provision Env ###
  ####################
  config.vm.provision "ansible_local" do |ansible|
    ansible.playbook = "pb.conf.all.yml"
    ansible.groups = {
      "routers" => ["site1router", "isp", "site2router"],
      "servers" => ["site1server", "site2server"],
      "all:children" => ["routers", "servers"]
    }
  end

end