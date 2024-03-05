# logging-receiver

Server able to receive Python [logging](https://docs.python.org/3/library/logging.html) records via TCP socket connection.

* collects log records from multiple processes or services
* central point to collect logs
* saves records to file in [JSON Lines](https://jsonlines.org/) format
* can rotate log files
* available as Docker container
* other services (such as [Elastic Stack](https://www.elastic.co/de/elastic-stack)) could pick up log files from this service

## Usage

Clone repository:

```
git clone https://github.com/matlabpackages/logging-receiver.git
cd logging-receiver
```

Copy example configuration and adjust `config.json` according to your needs:

```
cd example_config.json config.json
```

## References

Source code mostly taken from and inspired by:
* [Modern Python logging](https://www.youtube.com/watch?v=9L77QExPmI0)
* [Logging Cookbook](https://docs.python.org/3/howto/logging-cookbook.html)
