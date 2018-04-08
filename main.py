import get_config
import get_statement
import database

cfg = get_config.cfg

data = get_statement.statement(cfg['statement']['statementDir'])
database.insertTransaction(data)
