<?php

namespace App\FrontendModule;

use Nette,
	Nette\Diagnostics\Debugger;


/**
 *  @author Jan Mikes <j.mikes@me.com>
 *  @copyright Jan Mikes - janmikes.cz
 */
final class ErrorPresenter extends BasePresenter
{

	/**
	 * @param  Exception
	 * @return void
	 */
	public function renderDefault($exception)
	{
		if ($this->isAjax()) { // AJAX request? Just note this error in payload.
			$this->payload->error = TRUE;
			$this->terminate();

		} elseif ($exception instanceof Nette\Application\BadRequestException) {
			$code = $exception->getCode();
			// load template 403.latte or 404.latte or ... 4xx.latte
			$this->setView(in_array($code, array(403, 404, 405, 410, 500)) ? $code : '4xx');
			// Deliberately NOT logged to a file. Every 4xx used to append a line to
			// the Tracy log dir's access.log, which grows forever and is dominated by
			// vulnerability scanners probing /.env, /.git/HEAD and friends — that is
			// what let /app/log reach 2 GB inside the container. Apache's own access
			// log already records every request WITH its status code and goes to
			// stdout, so it is collected, retained and rotated centrally. Nothing is
			// lost by not duplicating it here; only 5xx (below) is a real error.

		} else {
			$this->setView('500'); // load template 500.latte
			Debugger::log($exception, Debugger::ERROR); // and log exception
		}
	}

}
