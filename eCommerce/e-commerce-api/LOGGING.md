# E-Commerce API Logging Documentation

## Overview

This document describes the comprehensive logging system implemented in the e-commerce API. The logging system provides structured, multi-level logging with file rotation and separate error tracking.

## Logging Levels

The API uses four standard logging levels:

### 1. DEBUG
- **Purpose**: Detailed information for diagnosing problems
- **Examples**: 
  - Database query details
  - Token validation steps
  - User lookup operations
  - Cart calculations

### 2. INFO
- **Purpose**: General informational messages about normal operations
- **Examples**:
  - User registration/login
  - Product creation/updates
  - Order placement
  - Cart operations
  - API request completion

### 3. WARNING
- **Purpose**: Indication of potential issues or unexpected situations
- **Examples**:
  - Failed authentication attempts
  - Product not found
  - Invalid token
  - Inactive user access attempts

### 4. ERROR
- **Purpose**: Error events that might still allow the application to continue
- **Examples**:
  - Database operation failures
  - Unexpected exceptions
  - Service errors
  - Token creation failures

## Log Files

The logging system creates log files in the `logs/` directory:

### Main Application Log
- **File**: `logs/ecommerce_api_YYYYMMDD.log`
- **Content**: All logs (DEBUG and above)
- **Rotation**: 10MB per file
- **Backups**: 5 files retained
- **Format**: `YYYY-MM-DD HH:MM:SS - logger_name - LEVEL - module:function:line - message`

### Error Log
- **File**: `logs/ecommerce_api_errors_YYYYMMDD.log`
- **Content**: Only ERROR level logs
- **Rotation**: 10MB per file
- **Backups**: 5 files retained
- **Purpose**: Quick access to critical errors

### Console Output
- **Level**: INFO and above
- **Purpose**: Real-time monitoring during development

## Logged Operations

### Authentication & Authorization
- User registration attempts and results
- Login attempts (success/failure)
- Token creation and validation
- Password hashing operations
- Current user validation
- Active user checks

### User Management
- User creation with duplicate checks
- User lookups by ID/username
- User profile access

### Product Operations
- Product listing with filters
- Product detail retrieval
- Product creation
- Product updates
- Category and search filtering

### Shopping Cart
- Cart retrieval
- Items added to cart
- Cart item updates
- Cart item removal
- Cart clearing
- Cart total calculations

### Order Processing
- Order creation from cart
- Order retrieval
- Order detail access
- Order item processing

### Database Operations
- Database engine initialization
- Session creation and cleanup
- Database connection errors
- Transaction failures

### HTTP Requests
- All incoming requests (method + path)
- Request completion with status code
- Response time for each request
- Request failures with error details

## Usage Examples

### Viewing Logs

#### View all logs for today
```bash
tail -f logs/ecommerce_api_$(date +%Y%m%d).log
```

#### View only errors
```bash
tail -f logs/ecommerce_api_errors_$(date +%Y%m%d).log
```

#### Filter specific operations
```bash
# View authentication logs
grep "Authentication" logs/ecommerce_api_*.log

# View order-related logs
grep "order" logs/ecommerce_api_*.log -i

# View failed operations
grep "failed" logs/ecommerce_api_*.log -i
```

### Log Analysis

#### Count errors by type
```bash
grep "ERROR" logs/ecommerce_api_*.log | cut -d'-' -f4 | sort | uniq -c
```

#### Find slow requests (> 1 second)
```bash
grep "Time: [1-9]" logs/ecommerce_api_*.log
```

#### Track user activity
```bash
grep "user: username" logs/ecommerce_api_*.log
```

## Configuration

### Changing Log Level
Edit `logger.py` and modify the `log_level` parameter in `setup_logger()`:

```python
logger = LoggerSetup.setup_logger(
    name="ecommerce_api",
    log_level="DEBUG"  # Change to INFO, WARNING, or ERROR
)
```

### Adjusting File Rotation
Modify the `max_bytes` and `backup_count` parameters:

```python
logger = LoggerSetup.setup_logger(
    max_bytes=10485760,  # 10MB (default)
    backup_count=5       # Keep 5 backup files
)
```

## Best Practices

### 1. Use Appropriate Log Levels
- DEBUG: Only for development/troubleshooting
- INFO: Normal operations users should know about
- WARNING: Potential issues that don't break functionality
- ERROR: Actual failures requiring attention

### 2. Include Context
All log messages include:
- Timestamp
- Module and function name
- Line number
- Relevant IDs (user ID, product ID, order ID)

### 3. Sensitive Data
The logging system automatically:
- Does NOT log passwords (plain or hashed)
- Does NOT log full token values
- Does NOT log credit card information
- Logs only usernames and IDs for tracking

### 4. Performance Monitoring
- Request/response times are logged
- Database operation durations can be added
- High-traffic endpoints are tracked

## Troubleshooting

### No logs appearing?
1. Check the `logs/` directory exists
2. Verify write permissions
3. Check if logging is initialized in `main.py`

### Log files too large?
1. Reduce `max_bytes` in `logger.py`
2. Decrease `backup_count`
3. Implement log archiving/cleanup script

### Missing specific logs?
1. Verify the log level is appropriate
2. Check if the code path is executed
3. Look for try-except blocks that might suppress logs

## Integration with Monitoring Tools

The structured log format is compatible with:
- **ELK Stack** (Elasticsearch, Logstash, Kibana)
- **Splunk**
- **Datadog**
- **CloudWatch** (AWS)
- **Application Insights** (Azure)

Example Logstash configuration:
```
input {
  file {
    path => "/path/to/logs/ecommerce_api_*.log"
    start_position => "beginning"
  }
}

filter {
  grok {
    match => { "message" => "%{TIMESTAMP_ISO8601:timestamp} - %{DATA:logger} - %{LOGLEVEL:level} - %{DATA:location} - %{GREEDYDATA:message}" }
  }
}

output {
  elasticsearch {
    hosts => ["localhost:9200"]
    index => "ecommerce-api-%{+YYYY.MM.dd}"
  }
}
```

## Maintenance

### Log Rotation
Logs automatically rotate based on size. Old logs are compressed and retained according to `backup_count`.

### Log Cleanup
Implement a scheduled task to remove old logs:

```bash
# Remove logs older than 30 days
find logs/ -name "*.log*" -mtime +30 -delete
```

### Monitoring Disk Space
```bash
# Check log directory size
du -sh logs/

# Monitor in real-time
watch -n 60 'du -sh logs/'
```

## Security Considerations

1. **Access Control**: Restrict log file access to authorized personnel only
2. **No Sensitive Data**: Passwords, tokens, and PII are not logged
3. **Log Tampering**: Consider implementing log signing for critical applications
4. **Audit Trail**: Logs provide a complete audit trail for compliance

## Future Enhancements

Potential improvements to the logging system:
1. Structured JSON logging for better parsing
2. Correlation IDs for request tracking
3. Performance metrics collection
4. Log aggregation to centralized service
5. Real-time alerting on specific error patterns
6. User action audit logs
