<?php

namespace App\FrontendModule;

use App,
	Nette;

/**
 *  @author Jan Mikes <j.mikes@me.com>
 *  @copyright Jan Mikes - janmikes.cz
 */
abstract class BasePresenter extends App\BasePresenter
{
	protected function beforeRender()
	{
		parent::beforeRender();

		$this->template->menuItems = array(
			"O nás" => "Homepage:",
			"Nabídka" => array(
				"Představení" => "Nabidka:predstaveni",
				"Putování" => "Nabidka:putovani",
				"Vyjížďky" => "Nabidka:vyjizdky",
				"Jezdecké kurzy" => "Nabidka:jezdeckeKurzy",
				"Filmy" => "Nabidka:filmy",
				"Přeprava koní" => "Nabidka:prepravaKoni",
			),
			"Fotogalerie" => "Fotogalerie:",
			"Kontakt" => "Kontakt:",
			"Spolupráce" => "Spoluprace:",
			"Vzkazník" => "Diskuse:",
		);
	}


	/** @return CssLoader */
	protected function createComponentCss()
	{
		return $this->webLoader->createCssLoader('frontend');
	}


	/** @return JavaScriptLoader */
	protected function createComponentJs()
	{
		return $this->webLoader->createJavaScriptLoader('frontend');
	}
}
