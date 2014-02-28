<?php

namespace App\Factories;

use Nette,
	Nette\Application\IPresenter,
	Nette\Application\UI,
	Nette\Templating\IFileTemplate,
	App;

/**
 *  @author Jan Mikes <j.mikes@me.com>
 *  @copyright Jan Mikes - janmikes.cz
 */
final class TemplateFactory extends Nette\Object {

	/** @var Nette\Localization\ITranslator */
	private $translator;

	/** @var string */
	private $appDir;

	/** @var Nette\Http\Response */
	private $httpResponse;

	/** @var Nette\Http\Request */
	private $httpRequest;

	/** @var Nette\Caching\IStorage */
	private $netteCacheStorage;

	/** @var Nette\Caching\IStorage */
	private $templateCacheStorage;

	/** @var App\Services\TemplateHelper */
	private $templateHelper;

	/** @var Nette\Application\Application */
	private $application;


	public function __construct(
		$appDir,
		$translator,
		Nette\Application\Application $application,
		Nette\Caching\IStorage $templateCacheStorage,
		Nette\Caching\IStorage $netteCacheStorage,
		Nette\Http\Response $httpResponse,
		Nette\Http\Request $httpRequest,
		App\Services\TemplateHelper $templateHelper
	) {
		$this->application = $application;
		$this->appDir = $appDir;
		$this->templateCacheStorage = $templateCacheStorage;;
		$this->netteCacheStorage = $netteCacheStorage;
		$this->httpResponse = $httpResponse;
		$this->httpRequest = $httpRequest;
		$this->translator = $translator;
		$this->templateHelper = $templateHelper;
	}


	/**
	 * Creates template and registers helpers and latte filter
	 * @param  UI\Control 	$control
	 * @param  string		$file	Filepath to file
	 * @param  string|NULL	$lang	Lang code (length=2)
	 * @param  string		$class	Name of template class
	 * @throws InvalidArgumentException
	 * @return Nette\Templating\IFileTemplate
	 */
	public function createTemplate(UI\Control $control, $file = NULL, $lang = NULL, $class = NULL)
	{

		$template = $class ? new $class : new Nette\Templating\FileTemplate;

		if (!$template instanceof IFileTemplate) {
			throw new \InvalidArgumentException('$template must be instance of Nette\\Templating\\IFileTemplate instead given ' . $class .' given!');
		}

		if (!is_null($this->translator)) {
			if ($lang) {
				$this->translator->setLangTo($lang);
			}
			$template->setTranslator($this->translator);
		}

		if (!is_null($file)) {
			$template->setFile($this->appDir . '/' . $file);
		}

		// default parameters
		$presenter = $control->getPresenter(FALSE);
		$template->control = $template->_control = $control;
		$template->presenter = $template->_presenter = $presenter;
		$template->basePath = "";
		if ($presenter instanceof UI\Presenter) {
			$template->setCacheStorage($this->templateCacheStorage);
			$template->user = $presenter->getUser();
			$template->netteHttpResponse = $this->httpResponse;
			$template->netteCacheStorage = $this->netteCacheStorage;
			$template->baseUri = $template->baseUrl = rtrim($this->httpRequest->getUrl()->getBaseUrl(), '/');
			$template->basePath = preg_replace('#https?://[^/]+#A', '', $template->baseUrl);

			// flash message
			if ($presenter->hasFlashSession()) {
				$id = $presenter->getParameterId('flash');
				$template->flashes = $presenter->getFlashSession()->$id;
			}
		}
		if (!isset($template->flashes) || !is_array($template->flashes)) {
			$template->flashes = array();
		}

		$template->registerHelperLoader('\Nette\Templating\Helpers::loader');
		$template->registerHelperLoader($this->templateHelper->loader);

		$latte = new Nette\Latte\Engine;
		$template->registerFilter($latte);

		return $template;
	}


	/**
	 * Creates email template
	 * @param  UI\Control $control
	 * @param  string      $file      path to file
	 * @param  string|NULL $lang
	 * @return Nette\Templating\IFileTemplate
	 */
	public function createEmailTemplate($name, $lang = null)
	{
		$file = "templates/emails/$name.latte";
		$template = $this->createTemplate($this->application->getPresenter(), $file, $lang);
		return $this->populateEmailTemplate($template);
	}


	/////////////////////
	// PRIVATE METHODS //
	/////////////////////


	/**
	 * Prepares variables for email template
	 * @param  Nette\Templating\IFileTemplate$template
	 * @return Nette\Templating\IFileTemplate
	 */
	private function populateEmailTemplate(IFileTemplate $template)
	{
		$template->s = array();

		return $template;
	}

}
