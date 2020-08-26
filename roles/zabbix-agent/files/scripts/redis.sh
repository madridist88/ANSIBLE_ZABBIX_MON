#!/bin/bash

HOST=$1
PORT=$2

function check() {
    pgrep redis-server | wc -l
}
function memory_used() {
    echo 'info memory' | redis-cli -h $HOST -p $PORT | grep -w used_memory | cut -d: -f2
}
function bgsave_status() {
    echo 'info persistence' | redis-cli -h $HOST -p $PORT| grep -c 'rdb_last_bgsave_status:ok'
}
function connected_clients() {
    echo 'info clients' | redis-cli -h $HOST -p $PORT| grep -w connected_clients | cut -d: -f2
}
function commands_processed() {
    echo 'info stats' | redis-cli -h $HOST -p $PORT| grep -w total_commands_processed | cut -d: -f2
}
function key_misses() {
        echo 'info stats' | redis-cli -h $HOST -p $PORT| grep -w keyspace_misses | cut -d: -f2
}
function key_hits() {
        echo 'info stats' | redis-cli -h $HOST -p $PORT| grep -w keyspace_hits | cut -d: -f2
}
function key_expirations() {
        echo 'info stats' | redis-cli -h $HOST -p $PORT| grep -w expired_keys | cut -d: -f2
}
function key_evictions() {
        echo 'info stats' | redis-cli -h $HOST -p $PORT| grep -w evicted_keys | cut -d: -f2
}
function master_sync_left_bytes() {
        echo 'info replication' | redis-cli -h $HOST -p $PORT| grep -w master_sync_left_bytes | cut -d: -f2
}
function connected_slaves() {
        echo 'info replication' | redis-cli -h $HOST -p $PORT| grep -w connected_slaves | cut -d: -f2
}
function slaves_changes() {
    prev=`cat /tmp/redis_slaves.txt`
    current=`echo 'info replication' | redis-cli -h $HOST -p $PORT| grep -w connected_slaves | cut -d: -f2`
    if [ "$prev" == "$current" ]; then
        echo "0"
    else
        echo "1"
    fi
    echo $current > /tmp/redis_slaves.txt
}
function slave_status() {
    role=`echo 'info replication' | redis-cli -h $HOST -p $PORT| grep -w role | cut -d: -f2`
    slaves_count=`echo 'info replication' | redis-cli -h $HOST -p $PORT| grep -w connected_slaves | cut -d: -f2`
    if [ "$role" == "slave" ]; then
        echo 'info replication' | redis-cli -h $HOST -p $PORT | grep -c 'master_link_status:up'
    fi
}
case "$3" in
        check)
                check;;
        memory_used)
        memory_used;;
    bgsave_status)
        bgsave_status;;
    connected_clients)
        connected_clients;;
    commands_processed)
        commands_processed;;
    key_misses)
        key_misses;;
    key_hits)
        key_hits;;
    key_expirations)
        key_expirations;;
    key_evictions)
        key_evictions;;
    master_sync_left_bytes)
        master_sync_left_bytes;;
    connected_slaves)
        connected_slaves;;
    slaves_changes)
        slaves_changes;;
    slave_status)
        slave_status;;
    *)
                echo $"Usage $0 {check|memory_used|bgsave_status|connected_clients|commands_processed|key_misses|key_hits|key_expirations|key_evictions|master_sync_left_bytes|connected_slaves}"
                exit
esac
