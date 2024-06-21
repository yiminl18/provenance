import logging
import datetime

def setup_logging(dir='test/output/logging', filename='langchain_civic_RAG_1'):
    """
    配置日志记录，只打印 'root - INFO' 级别的日志。
    """
    class RootInfoFilter(logging.Filter):
        def filter(self, record):
            return record.name == 'root' and record.levelname == 'INFO'

    # 获取当前时间戳
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

    # 配置日志记录
    log_filename = f'{dir}{filename}_{timestamp}.log'
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # 创建文件处理器和控制台处理器
    file_handler = logging.FileHandler(log_filename)
    console_handler = logging.StreamHandler()

    # 创建并添加过滤器
    filter = RootInfoFilter()
    file_handler.addFilter(filter)
    console_handler.addFilter(filter)

    # 设置格式化器
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # 添加处理器到logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger, file_handler, console_handler, timestamp

def close_logging(logger, handlers):
    """
    关闭日志记录器的处理器。
    """
    for handler in handlers:
        logger.removeHandler(handler)
        handler.close()


if __name__ == '__main__':
    # 调用日志配置函数
    setup_logging()

    # 示例函数
    def example_function(x, y):
        logging.info(f'Function called with x={x}, y={y}')
        result = x + y
        logging.info(f'Result of x + y = {result}')
        intermediate_result = result * 2
        logging.info(f'Intermediate result (result * 2) = {intermediate_result}')
        final_result = intermediate_result - 3
        logging.info(f'Final result (intermediate_result - 3) = {final_result}')
        return final_result

    # 调用示例函数
    example_function(5, 7)
