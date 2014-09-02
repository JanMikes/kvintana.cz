<?php

namespace App\Factories;

use Nette,
	App,
	App\Database\Entities\DiscussionEntity,
	Nette\Http\Request as HttpRequest;

/**
 *  @author Jan Mikes <j.mikes@me.com>
 *  @copyright Jan Mikes - janmikes.cz
 */
final class ManageDiscussionFormFactory extends Nette\Object
{
	use TFormSaveHandlers;


	/** @var App\Factories\FormFactory */
	private $formFactory;

	/** @var App\Database\Entities\DiscussionEntity */
	private $discussionEntity;

	/** @var Nette\Database\Table\ActiveRow */
	private $row;

	private $httpRequest;


	public function __construct(
		FormFactory $formFactory,
		DiscussionEntity $discussionEntity,
		HttpRequest $httpRequest
	) {
		$this->formFactory = $formFactory;
		$this->discussionEntity = $discussionEntity;
		$this->httpRequest = $httpRequest;
	}


	public function create($id)
	{
		if ($id) {
			$this->row = $this->discussionEntity->find($id);
		}

		$form = $this->formFactory->create();

		
		$form->addText("name", "Autor", 50, 50)
			->setRequired("Jméno je povinné!");

		$form->addText("email", "E-mail", 50, 50)
			->setRequired("E-mail je povinný!")
			->addRule($form::EMAIL, "Prosím zadejte e-mail ve správném tvaru!");

		$form->addTextarea("message", "Text", 50, 5)
			->setRequired("Zpráva je povinná!");
		

		$form->addSubmit("send", $this->row ? "Upravit" : "Přidat")
			->setAttribute("class", "btn-primary")
			->onClick[] = $this->save;

		if ($this->row) {
			$form->addSubmit("sendAndContinue", "Uložit a pokračovat v editaci")
				->setAttribute("class", "btn-primary")
				->onClick[] = $this->saveAndContinue;
		}

		return $form;
	}


	public function process(Nette\Application\UI\Form $form)
	{
		$values = $form->getValues(true);

		if (!$this->row) {
			$values["ins_process"] = __METHOD__;
			$values["remote_address"] = $this->httpRequest->remoteAddress;
			$values["remote_host"] = $this->httpRequest->remoteHost;
			$this->discussionEntity->insert($values);
		} else {
			$values["upd_process"] = __METHOD__;
			$this->row->update($values);
		}

	}

}
